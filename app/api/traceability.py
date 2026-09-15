"""Automatic requirement traceability matrix endpoints."""

from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Requirement, RequirementRelation


router = APIRouter(prefix="/traceability", tags=["traceability"])


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
