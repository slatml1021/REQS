"""Change impact analysis based on transitive traceability links."""

from fastapi import APIRouter, Depends, HTTPException
import networkx as nx
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Requirement, RequirementRelation


router = APIRouter(prefix="/impact-analysis", tags=["impact analysis"])


def _walk(graph: nx.MultiDiGraph, start_id: int) -> dict[int, tuple[int, list[str]]]:
    """Return shortest paths from NetworkX while preserving edge relation labels."""
    paths = nx.single_source_shortest_path(graph, start_id)
    found: dict[int, tuple[int, list[str]]] = {}
    for target_id, node_path in paths.items():
        if target_id == start_id:
            continue
        relation_path = [
            sorted(edge["relation_type"] for edge in graph.get_edge_data(source, target).values())[0]
            for source, target in zip(node_path, node_path[1:])
        ]
        found[target_id] = (len(node_path) - 1, relation_path)
    return found


@router.get("/{requirement_key}")
def impact_analysis(requirement_key: str, db: Session = Depends(get_db)) -> dict:
    """Return direct and transitive requirements affected in both link directions."""
    selected = db.scalar(select(Requirement).where(Requirement.key == requirement_key))
    if selected is None:
        raise HTTPException(status_code=404, detail="Requirement not found")
    requirements = {requirement.id: requirement for requirement in db.scalars(select(Requirement))}
    graph = nx.MultiDiGraph()
    graph.add_nodes_from(requirements)
    for relation in db.scalars(select(RequirementRelation)):
        graph.add_edge(relation.source_requirement_id, relation.target_requirement_id, relation_type=relation.relation_type.value)
        if not relation.is_directional:
            graph.add_edge(relation.target_requirement_id, relation.source_requirement_id, relation_type=relation.relation_type.value)
    affected = []
    for direction, directed_graph in (("forward", graph), ("backward", graph.reverse(copy=False))):
        for identifier, (distance, path) in _walk(directed_graph, selected.id).items():
            requirement = requirements[identifier]
            affected.append({"key": requirement.key, "title": requirement.title, "direction": direction, "distance": distance, "relation_path": path})
    return {"requirement_key": selected.key, "affected_requirements": sorted(affected, key=lambda item: (item["distance"], item["direction"], item["key"]))}
