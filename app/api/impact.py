"""Change impact analysis based on transitive traceability links."""

from collections import deque

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Requirement, RequirementRelation


router = APIRouter(prefix="/impact-analysis", tags=["impact analysis"])


def _walk(start_id: int, adjacency: dict[int, list[tuple[int, str]]]) -> dict[int, tuple[int, list[str]]]:
    visited: dict[int, tuple[int, list[str]]] = {}
    queue = deque([(start_id, 0, [])])
    while queue:
        node, distance, path = queue.popleft()
        for neighbor, relation_type in adjacency.get(node, []):
            if neighbor in visited or neighbor == start_id:
                continue
            next_path = path + [relation_type]
            visited[neighbor] = (distance + 1, next_path)
            queue.append((neighbor, distance + 1, next_path))
    return visited


@router.get("/{requirement_key}")
def impact_analysis(requirement_key: str, db: Session = Depends(get_db)) -> dict:
    """Return direct and transitive requirements affected in both link directions."""
    selected = db.scalar(select(Requirement).where(Requirement.key == requirement_key))
    if selected is None:
        raise HTTPException(status_code=404, detail="Requirement not found")
    requirements = {requirement.id: requirement for requirement in db.scalars(select(Requirement))}
    forward: dict[int, list[tuple[int, str]]] = {}
    backward: dict[int, list[tuple[int, str]]] = {}
    for relation in db.scalars(select(RequirementRelation)):
        forward.setdefault(relation.source_requirement_id, []).append((relation.target_requirement_id, relation.relation_type.value))
        backward.setdefault(relation.target_requirement_id, []).append((relation.source_requirement_id, relation.relation_type.value))
    affected = []
    for direction, graph in (("forward", forward), ("backward", backward)):
        for identifier, (distance, path) in _walk(selected.id, graph).items():
            requirement = requirements[identifier]
            affected.append({"key": requirement.key, "title": requirement.title, "direction": direction, "distance": distance, "relation_path": path})
    return {"requirement_key": selected.key, "affected_requirements": sorted(affected, key=lambda item: (item["distance"], item["direction"], item["key"]))}
