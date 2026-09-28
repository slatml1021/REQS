"""Karl Wiegers relative-weighting scoring endpoints."""

from decimal import Decimal

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import PriorityMethod, PriorityScore, Requirement
from app.schemas.wiegers import WiegersBatchWrite
from app.services import percent, wiegers_score


router = APIRouter(prefix="/wiegers", tags=["wiegers"])


@router.put("/scores")
def save_wiegers_scores(payload: WiegersBatchWrite, db: Session = Depends(get_db)) -> list[dict]:
    """Persist a batch of Wiegers assessments on a comparable 0-100 scale."""
    ids = {assessment.requirement_id for assessment in payload.assessments}
    requirements = {requirement.id: requirement for requirement in db.scalars(select(Requirement).where(Requirement.id.in_(ids)))}
    if set(requirements) != ids:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Requirement not found")
    weights = payload.weights.model_dump()
    try:
        raw_scores = {
            assessment.requirement_id: wiegers_score(assessment.benefit, assessment.penalty, assessment.cost, assessment.risk, weights)
            for assessment in payload.assessments
        }
    except ValueError as error:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_CONTENT, detail=str(error)) from error
    maximum = max(raw_scores.values())
    results = []
    for assessment in payload.assessments:
        raw_score = raw_scores[assessment.requirement_id].quantize(Decimal("0.0001"))
        normalized_score = percent(raw_score / maximum * Decimal(100))
        score = db.scalar(select(PriorityScore).where(PriorityScore.requirement_id == assessment.requirement_id, PriorityScore.method == PriorityMethod.WIEGERS))
        inputs = {"weights": {key: str(value) for key, value in weights.items()}, "ratings": {key: str(value) for key, value in assessment.model_dump(exclude={"requirement_id"}).items()}}
        if score is None:
            score = PriorityScore(requirement_id=assessment.requirement_id, method=PriorityMethod.WIEGERS, raw_score=raw_score, normalized_score=normalized_score, inputs=inputs)
            db.add(score)
        else:
            score.raw_score, score.normalized_score, score.inputs = raw_score, normalized_score, inputs
        results.append({"requirement_id": assessment.requirement_id, "requirement_key": requirements[assessment.requirement_id].key, "raw_score": float(raw_score), "normalized_score": float(normalized_score)})
    db.commit()
    return sorted(results, key=lambda item: (-item["normalized_score"], item["requirement_key"]))
