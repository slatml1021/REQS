"""CRUD endpoints for requirement traceability links."""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Requirement, RequirementRelation
from app.schemas.relation import RelationRead, RelationUpdate, RelationWrite


router = APIRouter(prefix="/relations", tags=["traceability"])


@router.get("", response_model=list[RelationRead])
def list_relations(db: Session = Depends(get_db)) -> list[RequirementRelation]:
    return list(db.scalars(select(RequirementRelation).order_by(RequirementRelation.source_requirement_id, RequirementRelation.target_requirement_id)))


@router.post("", response_model=RelationRead, status_code=status.HTTP_201_CREATED)
def create_relation(payload: RelationWrite, db: Session = Depends(get_db)) -> RequirementRelation:
    if len(set(db.scalars(select(Requirement.id).where(Requirement.id.in_({payload.source_requirement_id, payload.target_requirement_id}))))) != 2:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Requirement not found")
    relation = RequirementRelation(**payload.model_dump())
    db.add(relation)
    try:
        db.commit()
    except IntegrityError as error:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Relation already exists") from error
    db.refresh(relation)
    return relation


@router.patch("/{relation_id}", response_model=RelationRead)
def update_relation(
    relation_id: int, payload: RelationUpdate, db: Session = Depends(get_db)
) -> RequirementRelation:
    """Update the type or directionality of an existing traceability link."""
    relation = db.get(RequirementRelation, relation_id)
    if relation is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Relation not found")
    for field, value in payload.model_dump(exclude_unset=True).items():
        setattr(relation, field, value)
    try:
        db.commit()
    except IntegrityError as error:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Relation already exists") from error
    db.refresh(relation)
    return relation


@router.delete("/{relation_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_relation(relation_id: int, db: Session = Depends(get_db)) -> None:
    relation = db.get(RequirementRelation, relation_id)
    if relation is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Relation not found")
    db.delete(relation)
    db.commit()
