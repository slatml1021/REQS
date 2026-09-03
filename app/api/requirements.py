"""CRUD endpoints for the requirement backlog."""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Requirement
from app.schemas.requirement import RequirementCreate, RequirementRead, RequirementUpdate


router = APIRouter(prefix="/requirements", tags=["requirements"])


def _get_requirement_or_404(requirement_id: int, db: Session) -> Requirement:
    requirement = db.get(Requirement, requirement_id)
    if requirement is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Requirement not found")
    return requirement


@router.post("", response_model=RequirementRead, status_code=status.HTTP_201_CREATED)
def create_requirement(payload: RequirementCreate, db: Session = Depends(get_db)) -> Requirement:
    requirement = Requirement(**payload.model_dump())
    db.add(requirement)
    try:
        db.commit()
    except IntegrityError as error:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Requirement key already exists") from error
    db.refresh(requirement)
    return requirement


@router.get("", response_model=list[RequirementRead])
def list_requirements(db: Session = Depends(get_db)) -> list[Requirement]:
    return list(db.scalars(select(Requirement).order_by(Requirement.key)))


@router.get("/{requirement_id}", response_model=RequirementRead)
def get_requirement(requirement_id: int, db: Session = Depends(get_db)) -> Requirement:
    return _get_requirement_or_404(requirement_id, db)


@router.patch("/{requirement_id}", response_model=RequirementRead)
def update_requirement(
    requirement_id: int, payload: RequirementUpdate, db: Session = Depends(get_db)
) -> Requirement:
    requirement = _get_requirement_or_404(requirement_id, db)
    for field, value in payload.model_dump(exclude_unset=True).items():
        setattr(requirement, field, value)
    db.commit()
    db.refresh(requirement)
    return requirement


@router.delete("/{requirement_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_requirement(requirement_id: int, db: Session = Depends(get_db)) -> None:
    requirement = _get_requirement_or_404(requirement_id, db)
    db.delete(requirement)
    db.commit()
