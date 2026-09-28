"""Load the documented REQS case study without deleting unrelated project records."""

from __future__ import annotations

import argparse
import json
from decimal import Decimal
from itertools import combinations
from pathlib import Path

from sqlalchemy import select

from app.database import SessionLocal
from app.models import AhpComparison, PriorityMethod, PriorityScore, RelationType, Requirement, RequirementRelation
from app.services import ahp_priorities, percent, wiegers_score


DATA_PATH = Path(__file__).resolve().parents[1] / "sample_data" / "reqs_vaka_calismasi.json"
SAATY = [Decimal(1) / Decimal(number) for number in range(9, 1, -1)] + [Decimal(number) for number in range(1, 10)]


def nearest_saaty(value: Decimal) -> Decimal:
    return min(SAATY, key=lambda candidate: abs(candidate - value))


def upsert_score(db, requirement_id: int, method: PriorityMethod, raw: Decimal, normalized: Decimal, inputs: dict) -> None:
    score = db.scalar(select(PriorityScore).where(PriorityScore.requirement_id == requirement_id, PriorityScore.method == method))
    if score is None:
        db.add(PriorityScore(requirement_id=requirement_id, method=method, raw_score=raw, normalized_score=normalized, inputs=inputs))
    else:
        score.raw_score, score.normalized_score, score.inputs = raw, normalized, inputs


def load_case_study(reset: bool = False) -> dict:
    data = json.loads(DATA_PATH.read_text(encoding="utf-8"))
    db = SessionLocal()
    try:
        if reset:
            for requirement in db.scalars(select(Requirement).where(Requirement.key.like("REQS-%"))):
                db.delete(requirement)
            db.flush()
        requirements = {}
        for item in data["requirements"]:
            requirement = db.scalar(select(Requirement).where(Requirement.key == item["key"]))
            values = {key: item[key] for key in ("title", "description", "requirement_type", "status")}
            if requirement is None:
                requirement = Requirement(key=item["key"], **values)
                db.add(requirement)
                db.flush()
            else:
                for field, value in values.items():
                    setattr(requirement, field, value)
            requirements[item["key"]] = requirement
        db.flush()

        for source_key, target_key, relation_name, is_directional in data["relations"]:
            source, target = requirements[source_key], requirements[target_key]
            relation_type = RelationType(relation_name)
            relation = db.scalar(select(RequirementRelation).where(RequirementRelation.source_requirement_id == source.id, RequirementRelation.target_requirement_id == target.id, RequirementRelation.relation_type == relation_type))
            if relation is None:
                db.add(RequirementRelation(source_requirement_id=source.id, target_requirement_id=target.id, relation_type=relation_type, is_directional=is_directional))
            else:
                relation.is_directional = is_directional
        db.flush()

        ordered = [requirements[item["key"]] for item in data["requirements"]]
        ranks = {requirements[item["key"]].id: Decimal(item["ahp_rank"]) for item in data["requirements"]}
        for left, right in combinations(ordered, 2):
            comparison_value = nearest_saaty(ranks[left.id] / ranks[right.id])
            pair = db.scalar(select(AhpComparison).where(AhpComparison.requirement_a_id == left.id, AhpComparison.requirement_b_id == right.id))
            if pair is None:
                db.add(AhpComparison(requirement_a_id=left.id, requirement_b_id=right.id, comparison_value=comparison_value))
            else:
                pair.comparison_value = comparison_value
        db.flush()
        matrix = [[Decimal(1) if row.id == column.id else nearest_saaty(ranks[row.id] / ranks[column.id]) for column in ordered] for row in ordered]
        priorities, consistency_ratio = ahp_priorities(matrix)
        for requirement, priority in zip(ordered, priorities, strict=True):
            upsert_score(db, requirement.id, PriorityMethod.AHP, priority.quantize(Decimal("0.0001")), percent(priority * 100), {"priority_weight": str(priority), "consistency_ratio": str(consistency_ratio)})

        weights = {"benefit": Decimal(1), "penalty": Decimal(1), "cost": Decimal(1), "risk": Decimal(1)}
        raw_wiegers = {}
        for item in data["requirements"]:
            benefit, penalty, cost, risk = map(Decimal, item["wiegers"])
            raw_wiegers[requirements[item["key"]].id] = wiegers_score(benefit, penalty, cost, risk, weights)
        maximum = max(raw_wiegers.values())
        for item in data["requirements"]:
            requirement = requirements[item["key"]]
            raw = raw_wiegers[requirement.id]
            upsert_score(db, requirement.id, PriorityMethod.WIEGERS, raw.quantize(Decimal("0.0001")), percent(raw / maximum * 100), {"weights": {key: str(value) for key, value in weights.items()}, "ratings": item["wiegers"]})

        for item in data["requirements"]:
            requirement = requirements[item["key"]]
            raw = sum(Decimal(weight) * Decimal(score) / 100 for (_, weight), score in zip(data["volere_criteria"], item["volere"], strict=True))
            upsert_score(db, requirement.id, PriorityMethod.VOLERE, raw.quantize(Decimal("0.0001")), percent(raw * 10), {"criteria": [{"name": name, "weight": weight, "score": score} for (name, weight), score in zip(data["volere_criteria"], item["volere"], strict=True)]})
        db.commit()
        return {"requirements": len(requirements), "relations": len(data["relations"]), "consistency_ratio": float(consistency_ratio)}
    finally:
        db.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--reset", action="store_true", help="Only reset records whose keys begin with REQS-.")
    arguments = parser.parse_args()
    print(json.dumps(load_case_study(reset=arguments.reset), ensure_ascii=False, indent=2))
