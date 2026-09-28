"""Pure calculation services used by REQS API routes."""

from __future__ import annotations

from decimal import Decimal, ROUND_HALF_UP
import numpy as np


RI_VALUES = {1: 0.0, 2: 0.0, 3: 0.58, 4: 0.90, 5: 1.12, 6: 1.24, 7: 1.32, 8: 1.41, 9: 1.45, 10: 1.49}


def ahp_priorities(matrix: list[list[Decimal]]) -> tuple[list[Decimal], Decimal]:
    """Return geometric-mean AHP weights and Saaty's consistency ratio."""
    size = len(matrix)
    if size == 0 or any(len(row) != size for row in matrix):
        raise ValueError("AHP matrix must be square")
    eigenvalues, eigenvectors = np.linalg.eig(np.array([[float(value) for value in row] for row in matrix], dtype=float))
    principal = int(np.argmax(eigenvalues.real))
    vector = np.abs(eigenvectors[:, principal].real)
    priorities = [Decimal(str(float(value / vector.sum()))) for value in vector]
    lambda_max = Decimal(str(float(eigenvalues[principal].real)))
    consistency_index = (lambda_max - size) / (size - 1) if size > 1 else Decimal(0)
    random_index = Decimal(str(RI_VALUES.get(size, RI_VALUES[10])))
    consistency_ratio = max(Decimal(0), consistency_index / random_index) if random_index else Decimal(0)
    return priorities, consistency_ratio


def wiegers_score(benefit: Decimal, penalty: Decimal, cost: Decimal, risk: Decimal, weights: dict[str, Decimal]) -> Decimal:
    """Calculate Karl Wiegers' weighted relative-priority score."""
    denominator = (cost * weights["cost"]) + (risk * weights["risk"])
    if denominator <= 0:
        raise ValueError("Wiegers cost and risk denominator must be positive")
    return ((benefit * weights["benefit"]) + (penalty * weights["penalty"])) / denominator


def percent(value: Decimal) -> Decimal:
    return value.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
