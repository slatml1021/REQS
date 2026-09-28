"""Persistence endpoints for AHP pairwise judgments."""

from decimal import Decimal, InvalidOperation

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import AhpComparison, PriorityMethod, PriorityScore, Requirement
from app.schemas.ahp import AhpComparisonRead, AhpComparisonWrite
from app.services import ahp_priorities, percent


router = APIRouter(prefix="/ahp/comparisons", tags=["ahp"])

SAATY_VALUES = {Decimal(number) for number in range(1, 10)} | {
    Decimal(1) / Decimal(number) for number in range(2, 10)
}


def _parse_saaty_value(raw_value: str) -> Decimal:
    try:
        if "/" in raw_value:
            numerator, denominator = raw_value.split("/", maxsplit=1)
            value = Decimal(numerator) / Decimal(denominator)
        else:
            value = Decimal(raw_value)
    except (InvalidOperation, ValueError, ZeroDivisionError) as error:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_CONTENT, detail="Invalid Saaty value") from error
    if value not in SAATY_VALUES:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_CONTENT, detail="Saaty value must be between 1/9 and 9")
    return value


@router.put("", response_model=AhpComparisonRead)
def save_comparison(payload: AhpComparisonWrite, db: Session = Depends(get_db)) -> AhpComparison:
    if payload.left_requirement_id == payload.right_requirement_id:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_CONTENT, detail="Requirements must be different")

    required_ids = {payload.left_requirement_id, payload.right_requirement_id}
    found_ids = set(db.scalars(select(Requirement.id).where(Requirement.id.in_(required_ids))))
    if found_ids != required_ids:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Requirement not found")

    value = _parse_saaty_value(payload.comparison_value)
    requirement_a_id, requirement_b_id = sorted(required_ids)
    if payload.left_requirement_id != requirement_a_id:
        value = Decimal(1) / value

    comparison = db.scalar(
        select(AhpComparison).where(
            AhpComparison.requirement_a_id == requirement_a_id,
            AhpComparison.requirement_b_id == requirement_b_id,
        )
    )
    if comparison is None:
        comparison = AhpComparison(
            requirement_a_id=requirement_a_id,
            requirement_b_id=requirement_b_id,
            comparison_value=value,
        )
        db.add(comparison)
    else:
        comparison.comparison_value = value
    db.commit()
    db.refresh(comparison)
    return comparison


@router.get("", response_model=list[AhpComparisonRead])
def list_comparisons(db: Session = Depends(get_db)) -> list[AhpComparison]:
    return list(db.scalars(select(AhpComparison).order_by(AhpComparison.requirement_a_id, AhpComparison.requirement_b_id)))


@router.post("/calculate")
def calculate_ahp(db: Session = Depends(get_db)) -> dict:
    """Calculate and persist AHP weights from all saved pairwise judgments."""
    requirements = list(db.scalars(select(Requirement).order_by(Requirement.id)))
    if not requirements:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_CONTENT, detail="At least one requirement is needed")
    ids = [requirement.id for requirement in requirements]
    comparisons = {
        (comparison.requirement_a_id, comparison.requirement_b_id): comparison.comparison_value
        for comparison in db.scalars(select(AhpComparison))
    }
    missing = [(ids[left], ids[right]) for left in range(len(ids)) for right in range(left + 1, len(ids)) if (ids[left], ids[right]) not in comparisons]
    if missing:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_CONTENT, detail={"message": "All requirement pairs must be compared", "missing_pairs": missing})
    matrix = []
    for row_id in ids:
        row = []
        for column_id in ids:
            if row_id == column_id:
                row.append(Decimal(1))
            elif row_id < column_id:
                row.append(comparisons[(row_id, column_id)])
            else:
                row.append(Decimal(1) / comparisons[(column_id, row_id)])
        matrix.append(row)
    priorities, consistency_ratio = ahp_priorities(matrix)
    output = []
    for requirement, priority in zip(requirements, priorities, strict=True):
        normalized_score = percent(priority * Decimal(100))
        score = db.scalar(select(PriorityScore).where(PriorityScore.requirement_id == requirement.id, PriorityScore.method == PriorityMethod.AHP))
        inputs = {"priority_weight": str(priority), "consistency_ratio": str(consistency_ratio)}
        if score is None:
            score = PriorityScore(requirement_id=requirement.id, method=PriorityMethod.AHP, raw_score=priority.quantize(Decimal("0.0001")), normalized_score=normalized_score, inputs=inputs)
            db.add(score)
        else:
            score.raw_score, score.normalized_score, score.inputs = priority.quantize(Decimal("0.0001")), normalized_score, inputs
        output.append({"requirement_id": requirement.id, "requirement_key": requirement.key, "normalized_score": float(normalized_score)})
    db.commit()
    return {"consistency_ratio": float(consistency_ratio), "is_consistent": consistency_ratio < Decimal("0.10"), "results": sorted(output, key=lambda item: -item["normalized_score"])}
