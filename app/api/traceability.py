"""Automatic requirement traceability matrix endpoints."""

from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Requirement, RequirementRelation


router = APIRouter(prefix="/traceability", tags=["traceability"])


def _requirement_payload(requirement: Requirement) -> dict:
    return {"id": requirement.id, "key": requirement.key, "title": requirement.title}


@router.get("/matrix")
def traceability_matrix(db: Session = Depends(get_db)) -> dict:
    """Derive a directed relationship matrix from the canonical relation records."""
    requirements = list(db.scalars(select(Requirement).order_by(Requirement.key)))
    relations = list(db.scalars(select(RequirementRelation)))
    keys = [requirement.key for requirement in requirements]
    id_to_key = {requirement.id: requirement.key for requirement in requirements}
    cells = {source: {target: [] for target in keys} for source in keys}
    for relation in relations:
        source = id_to_key.get(relation.source_requirement_id)
        target = id_to_key.get(relation.target_requirement_id)
        if source and target:
            cells[source][target].append(relation.relation_type.value)
    return {"requirements": keys, "matrix": cells}


@router.get("/{requirement_key}/forward")
def forward_traceability(requirement_key: str, db: Session = Depends(get_db)) -> dict:
    """List direct targets of a requirement's directed traceability links."""
    source = db.scalar(select(Requirement).where(Requirement.key == requirement_key))
    if source is None:
        return {"requirement_key": requirement_key, "relations": []}
    rows = db.execute(
        select(RequirementRelation, Requirement)
        .join(Requirement, RequirementRelation.target_requirement_id == Requirement.id)
        .where(RequirementRelation.source_requirement_id == source.id)
        .order_by(Requirement.key, RequirementRelation.relation_type)
    )
    return {
        "requirement_key": source.key,
        "relations": [
            {"relation_type": relation.relation_type.value, "requirement": _requirement_payload(target)}
            for relation, target in rows
        ],
    }


@router.get("/{requirement_key}/backward")
def backward_traceability(requirement_key: str, db: Session = Depends(get_db)) -> dict:
    """List direct sources of a requirement's directed traceability links."""
    target = db.scalar(select(Requirement).where(Requirement.key == requirement_key))
    if target is None:
        return {"requirement_key": requirement_key, "relations": []}
    rows = db.execute(
        select(RequirementRelation, Requirement)
        .join(Requirement, RequirementRelation.source_requirement_id == Requirement.id)
        .where(RequirementRelation.target_requirement_id == target.id)
        .order_by(Requirement.key, RequirementRelation.relation_type)
    )
    return {
        "requirement_key": target.key,
        "relations": [
            {"relation_type": relation.relation_type.value, "requirement": _requirement_payload(source)}
            for relation, source in rows
        ],
    }
