"""End-to-end acceptance scenarios derived from Sıla Temel's REQS checklist."""

from itertools import combinations
from time import perf_counter

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.database import Base, get_db
from app.main import app


@pytest.fixture
def client():
    engine = create_engine(
        "sqlite://", connect_args={"check_same_thread": False}, poolclass=StaticPool
    )
    session_factory = sessionmaker(bind=engine, autoflush=False, autocommit=False)
    Base.metadata.create_all(engine)

    def override_get_db():
        db = session_factory()
        try:
            yield db
        finally:
            db.close()

    previous_overrides = app.dependency_overrides.copy()
    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()
    app.dependency_overrides.update(previous_overrides)
    Base.metadata.drop_all(engine)


def create_requirements(client: TestClient, count: int) -> list[dict]:
    return [
        client.post(
            "/api/v1/requirements",
            json={"key": f"REQ-{number:03}", "title": f"Örnek gereksinim {number}"},
        ).json()
        for number in range(1, count + 1)
    ]


def test_five_requirement_scenario_covers_core_acceptance_criteria(client: TestClient):
    """Three methods, dynamic traceability, impact analysis, dashboard and PDF work together."""
    requirements = create_requirements(client, 5)
    ids = [requirement["id"] for requirement in requirements]

    for left, right in combinations(ids, 2):
        assert client.put(
            "/api/v1/ahp/comparisons",
            json={
                "left_requirement_id": left,
                "right_requirement_id": right,
                "comparison_value": "1",
            },
        ).status_code == 200
    ahp = client.post("/api/v1/ahp/comparisons/calculate")
    assert ahp.status_code == 200
    assert ahp.json()["is_consistent"] is True

    wiegers = client.put(
        "/api/v1/wiegers/scores",
        json={
            "weights": {"benefit": 1, "penalty": 1, "cost": 1, "risk": 1},
            "assessments": [
                {
                    "requirement_id": requirement_id,
                    "benefit": 9 - offset,
                    "penalty": 8 - offset,
                    "cost": 1 + offset,
                    "risk": 1 + offset,
                }
                for offset, requirement_id in enumerate(ids)
            ],
        },
    )
    assert wiegers.status_code == 200
    assert [result["requirement_id"] for result in wiegers.json()] == ids

    for offset, requirement_id in enumerate(ids):
        volere = client.put(
            "/api/v1/volere/scores",
            json={
                "requirement_id": requirement_id,
                "criteria": [
                    {"name": "Müşteri değeri", "weight": 40, "score": 9 - offset},
                    {"name": "İş değeri", "weight": 30, "score": 8 - offset},
                    {"name": "Uygulama kolaylığı", "weight": 20, "score": 7 - offset},
                    {"name": "Maliyet avantajı", "weight": 10, "score": 6 - offset},
                ],
            },
        )
        assert volere.status_code == 200

    results = client.get("/api/v1/prioritization/results")
    assert results.status_code == 200
    assert len(results.json()) == 15
    assert {result["method"] for result in results.json()} == {"ahp", "wiegers", "volere"}
    assert all(0 <= result["normalized_score"] <= 100 for result in results.json())

    relations = [
        (ids[0], ids[1], "depends_on"),
        (ids[1], ids[2], "prerequisite_of"),
        (ids[2], ids[3], "refines"),
        (ids[3], ids[4], "related_to"),
    ]
    created_relations = []
    for source_id, target_id, relation_type in relations:
        response = client.post(
            "/api/v1/relations",
            json={
                "source_requirement_id": source_id,
                "target_requirement_id": target_id,
                "relation_type": relation_type,
            },
        )
        assert response.status_code == 201
        created_relations.append(response.json())

    matrix = client.get("/api/v1/traceability/matrix").json()
    assert matrix["requirements"] == [requirement["key"] for requirement in requirements]
    assert matrix["matrix"]["REQ-001"]["REQ-002"] == ["depends_on"]
    assert matrix["matrix"]["REQ-003"]["REQ-004"] == ["refines"]
    assert client.get("/api/v1/traceability/REQ-002/backward").json()["relations"][0]["requirement"]["key"] == "REQ-001"
    assert client.get("/api/v1/traceability/REQ-002/forward").json()["relations"][0]["requirement"]["key"] == "REQ-003"

    impact = client.get("/api/v1/impact-analysis/REQ-003")
    assert impact.status_code == 200
    assert {(item["key"], item["direction"], item["distance"]) for item in impact.json()["affected_requirements"]} == {
        ("REQ-001", "backward", 2),
        ("REQ-002", "backward", 1),
        ("REQ-004", "forward", 1),
        ("REQ-005", "forward", 2),
    }

    assert client.delete(f"/api/v1/relations/{created_relations[-1]['id']}").status_code == 204
    refreshed_matrix = client.get("/api/v1/traceability/matrix").json()
    assert refreshed_matrix["matrix"]["REQ-004"]["REQ-005"] == []

    assert "chart.js" in client.get("/prioritization/dashboard").text.lower()
    graph = client.get("/traceability/graph")
    assert "vis-network" in graph.text.lower()
    assert "/api/v1/traceability/graph" in graph.text
    pdf = client.get("/api/v1/reports/pdf")
    assert pdf.status_code == 200
    assert pdf.headers["content-type"].startswith("application/pdf")
    assert pdf.content.startswith(b"%PDF")


def test_ahp_inconsistent_comparisons_produce_a_consistency_warning(client: TestClient):
    requirements = create_requirements(client, 3)
    first, second, third = [requirement["id"] for requirement in requirements]
    for left, right, value in ((first, second, "9"), (second, third, "9"), (first, third, "1")):
        assert client.put(
            "/api/v1/ahp/comparisons",
            json={"left_requirement_id": left, "right_requirement_id": right, "comparison_value": value},
        ).status_code == 200

    result = client.post("/api/v1/ahp/comparisons/calculate")
    assert result.status_code == 200
    assert result.json()["is_consistent"] is False
    assert result.json()["consistency_ratio"] > 0.10


def test_volere_rejects_more_than_four_criteria_and_invalid_wiegers_inputs(client: TestClient):
    requirement_id = create_requirements(client, 1)[0]["id"]
    assert client.put(
        "/api/v1/volere/scores",
        json={
            "requirement_id": requirement_id,
            "criteria": [
                {"name": f"Kriter {number}", "weight": 20, "score": 5}
                for number in range(1, 6)
            ],
        },
    ).status_code == 422
    assert client.put(
        "/api/v1/wiegers/scores",
        json={
            "weights": {"benefit": 1, "penalty": 1, "cost": 1, "risk": 1},
            "assessments": [
                {"requirement_id": requirement_id, "benefit": 10, "penalty": 1, "cost": 1, "risk": 1}
            ],
        },
    ).status_code == 422


def test_traceability_matrix_handles_one_hundred_requirements(client: TestClient):
    """Record a lightweight 100-requirement matrix observation from the acceptance checklist."""
    create_requirements(client, 100)
    started_at = perf_counter()
    response = client.get("/api/v1/traceability/matrix")
    elapsed_seconds = perf_counter() - started_at

    assert response.status_code == 200
    assert len(response.json()["requirements"]) == 100
    assert len(response.json()["matrix"]) == 100
    assert elapsed_seconds < 5
