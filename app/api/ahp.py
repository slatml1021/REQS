"""Persistence endpoints for AHP pairwise judgments."""

from decimal import Decimal, InvalidOperation

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import AhpComparison, Requirement
from app.schemas.ahp import AhpComparisonRead, AhpComparisonWrite


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
