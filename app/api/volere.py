"""Volere weighted scoring endpoints."""

from decimal import Decimal, ROUND_HALF_UP

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import PriorityMethod, PriorityScore, Requirement
from app.schemas.volere import VolereScoreRead, VolereScoreWrite


router = APIRouter(prefix="/volere", tags=["volere"])


@router.put("/scores", response_model=VolereScoreRead)
def save_volere_score(payload: VolereScoreWrite, db: Session = Depends(get_db)) -> PriorityScore:
    """Validate a Volere assessment, calculate its weighted score and persist it."""
    if db.get(Requirement, payload.requirement_id) is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Requirement not found")

    total_weight = sum((criterion.weight for criterion in payload.criteria), Decimal(0))
    if total_weight != Decimal(100):
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_CONTENT, detail="Criterion weights must total 100")
    if len({criterion.name.strip().casefold() for criterion in payload.criteria}) != len(payload.criteria):
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_CONTENT, detail="Criterion names must be unique")

    raw_score = sum((criterion.weight * criterion.score / Decimal(100) for criterion in payload.criteria), Decimal(0))
    raw_score = raw_score.quantize(Decimal("0.0001"), rounding=ROUND_HALF_UP)
    normalized_score = (raw_score * Decimal(10)).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
    inputs = {"criteria": [criterion.model_dump(mode="json") for criterion in payload.criteria]}

    priority_score = db.scalar(
        select(PriorityScore).where(
            PriorityScore.requirement_id == payload.requirement_id,
            PriorityScore.method == PriorityMethod.VOLERE,
        )
    )
    if priority_score is None:
        priority_score = PriorityScore(
            requirement_id=payload.requirement_id,
            method=PriorityMethod.VOLERE,
            raw_score=raw_score,
            normalized_score=normalized_score,
            inputs=inputs,
        )
        db.add(priority_score)
    else:
        priority_score.raw_score = raw_score
        priority_score.normalized_score = normalized_score
        priority_score.inputs = inputs
    db.commit()
    db.refresh(priority_score)
    return priority_score
