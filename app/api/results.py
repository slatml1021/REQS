"""Common, method-neutral prioritization result view."""

from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import PriorityScore, Requirement


router = APIRouter(prefix="/prioritization", tags=["prioritization"])


@router.get("/results")
def list_results(db: Session = Depends(get_db)) -> list[dict]:
    """Return all persisted method scores in one comparable 0–100 scale."""
    rows = db.execute(
        select(PriorityScore, Requirement.key, Requirement.title)
        .join(Requirement, PriorityScore.requirement_id == Requirement.id)
        .order_by(PriorityScore.method, PriorityScore.normalized_score.desc(), Requirement.key)
    )
    return [
        {
            "requirement_id": score.requirement_id,
            "requirement_key": key,
            "requirement_title": title,
            "method": score.method.value,
            "raw_score": float(score.raw_score),
            "normalized_score": float(score.normalized_score),
        }
        for score, key, title in rows
    ]
