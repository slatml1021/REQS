from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.database import Base, get_db
from app.main import app


engine = create_engine("sqlite://", connect_args={"check_same_thread": False}, poolclass=StaticPool)
TestingSessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)


def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db
client = TestClient(app)


def setup_function():
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)


def test_requirement_crud_lifecycle():
    created = client.post("/api/v1/requirements", json={"key": "REQ-001", "title": "Kullanıcı girişi"})
    assert created.status_code == 201
    requirement_id = created.json()["id"]

    listed = client.get("/api/v1/requirements")
    assert listed.status_code == 200
    assert [item["key"] for item in listed.json()] == ["REQ-001"]

    updated = client.patch(f"/api/v1/requirements/{requirement_id}", json={"status": "approved"})
    assert updated.status_code == 200
    assert updated.json()["status"] == "approved"

    deleted = client.delete(f"/api/v1/requirements/{requirement_id}")
    assert deleted.status_code == 204
    assert client.get(f"/api/v1/requirements/{requirement_id}").status_code == 404


def test_duplicate_requirement_key_is_rejected():
    payload = {"key": "REQ-001", "title": "Kullanıcı girişi"}
    assert client.post("/api/v1/requirements", json=payload).status_code == 201
    assert client.post("/api/v1/requirements", json=payload).status_code == 409


def test_ahp_screen_renders_requirement_choices():
    client.post("/api/v1/requirements", json={"key": "REQ-001", "title": "Kullanıcı girişi"})
    client.post("/api/v1/requirements", json={"key": "REQ-002", "title": "Rapor üretimi"})

    response = client.get("/ahp/comparisons")

    assert response.status_code == 200
    assert "AHP ikili karşılaştırma" in response.text
    assert "REQ-001 — Kullanıcı girişi" in response.text
    assert "REQ-002 — Rapor üretimi" in response.text


def test_volere_screen_renders_criteria_and_requirement_choice():
    client.post("/api/v1/requirements", json={"key": "REQ-001", "title": "Kullanıcı girişi"})

    response = client.get("/volere/scoring")

    assert response.status_code == 200
    assert "Volere kriter ve puanlama" in response.text
    assert "Müşteri değeri" in response.text
    assert "REQ-001 — Kullanıcı girişi" in response.text


def test_volere_score_is_calculated_and_updated():
    requirement_id = client.post("/api/v1/requirements", json={"key": "REQ-001", "title": "Kullanıcı girişi"}).json()["id"]
    payload = {
        "requirement_id": requirement_id,
        "criteria": [
            {"name": "Müşteri değeri", "weight": 40, "score": 10},
            {"name": "İş değeri", "weight": 30, "score": 8},
            {"name": "Uygulama kolaylığı", "weight": 20, "score": 5},
            {"name": "Maliyet avantajı", "weight": 10, "score": 0},
        ],
    }

    saved = client.put("/api/v1/volere/scores", json=payload)
    payload["criteria"][0]["score"] = 5
    updated = client.put("/api/v1/volere/scores", json=payload)

    assert saved.status_code == 200
    assert saved.json()["raw_score"] == "7.4000"
    assert saved.json()["normalized_score"] == "74.00"
    assert updated.status_code == 200
    assert updated.json()["normalized_score"] == "54.00"


def test_volere_score_requires_weights_to_total_one_hundred():
    requirement_id = client.post("/api/v1/requirements", json={"key": "REQ-001", "title": "Kullanıcı girişi"}).json()["id"]
    response = client.put(
        "/api/v1/volere/scores",
        json={"requirement_id": requirement_id, "criteria": [{"name": "Değer", "weight": 90, "score": 8}]},
    )
    assert response.status_code == 422


def test_common_results_exposes_normalized_volere_score():
    requirement_id = client.post("/api/v1/requirements", json={"key": "REQ-001", "title": "Kullanıcı girişi"}).json()["id"]
    client.put(
        "/api/v1/volere/scores",
        json={"requirement_id": requirement_id, "criteria": [{"name": "Değer", "weight": 100, "score": 8}]},
    )
    response = client.get("/api/v1/prioritization/results")
    assert response.status_code == 200
    assert response.json() == [{"requirement_id": requirement_id, "requirement_key": "REQ-001", "requirement_title": "Kullanıcı girişi", "method": "volere", "raw_score": 8.0, "normalized_score": 80.0}]


def test_traceability_matrix_is_derived_from_requirement_relations():
    first = client.post("/api/v1/requirements", json={"key": "REQ-001", "title": "Giriş"}).json()["id"]
    second = client.post("/api/v1/requirements", json={"key": "REQ-002", "title": "Rapor"}).json()["id"]
    from app.models import RelationType, RequirementRelation
    db = TestingSessionLocal()
    db.add(RequirementRelation(source_requirement_id=second, target_requirement_id=first, relation_type=RelationType.DEPENDS_ON))
    db.commit()
    db.close()

    response = client.get("/api/v1/traceability/matrix")
    assert response.status_code == 200
    assert response.json()["matrix"]["REQ-002"]["REQ-001"] == ["depends_on"]


def test_traceability_graph_screen_uses_matrix_endpoint():
    response = client.get("/traceability/graph")

    assert response.status_code == 200
    assert "İzlenebilirlik ilişki ağı" in response.text
    assert "/api/v1/traceability/matrix" in response.text


def test_forward_and_backward_traceability_follow_relation_direction():
    source_id = client.post("/api/v1/requirements", json={"key": "REQ-001", "title": "Giriş"}).json()["id"]
    target_id = client.post("/api/v1/requirements", json={"key": "REQ-002", "title": "Rapor"}).json()["id"]
    from app.models import RelationType, RequirementRelation

    db = TestingSessionLocal()
    db.add(
        RequirementRelation(
            source_requirement_id=source_id,
            target_requirement_id=target_id,
            relation_type=RelationType.REFINES,
        )
    )
    db.commit()
    db.close()

    forward = client.get("/api/v1/traceability/REQ-001/forward")
    backward = client.get("/api/v1/traceability/REQ-002/backward")

    assert forward.status_code == 200
    assert forward.json()["relations"] == [{"relation_type": "refines", "requirement": {"id": target_id, "key": "REQ-002", "title": "Rapor"}}]
    assert backward.status_code == 200
    assert backward.json()["relations"] == [{"relation_type": "refines", "requirement": {"id": source_id, "key": "REQ-001", "title": "Giriş"}}]


def test_traceability_direction_queries_are_empty_for_unknown_requirement():
    assert client.get("/api/v1/traceability/REQ-999/forward").json()["relations"] == []
    assert client.get("/api/v1/traceability/REQ-999/backward").json()["relations"] == []


def test_ahp_calculation_persists_consistent_priorities():
    first = client.post("/api/v1/requirements", json={"key": "REQ-001", "title": "Giriş"}).json()["id"]
    second = client.post("/api/v1/requirements", json={"key": "REQ-002", "title": "Rapor"}).json()["id"]
    assert client.put("/api/v1/ahp/comparisons", json={"left_requirement_id": first, "right_requirement_id": second, "comparison_value": "3"}).status_code == 200

    result = client.post("/api/v1/ahp/comparisons/calculate")

    assert result.status_code == 200
    assert result.json()["is_consistent"] is True
    assert result.json()["results"][0]["requirement_key"] == "REQ-001"
    assert client.get("/api/v1/prioritization/results").json()[0]["method"] == "ahp"


def test_wiegers_batch_calculates_comparable_scores():
    first = client.post("/api/v1/requirements", json={"key": "REQ-001", "title": "Giriş"}).json()["id"]
    second = client.post("/api/v1/requirements", json={"key": "REQ-002", "title": "Rapor"}).json()["id"]
    response = client.put("/api/v1/wiegers/scores", json={"weights": {"benefit": 1, "penalty": 1, "cost": 1, "risk": 1}, "assessments": [{"requirement_id": first, "benefit": 9, "penalty": 9, "cost": 1, "risk": 1}, {"requirement_id": second, "benefit": 1, "penalty": 1, "cost": 9, "risk": 9}]})

    assert response.status_code == 200
    assert response.json()[0]["requirement_key"] == "REQ-001"
    assert response.json()[0]["normalized_score"] == 100.0


def test_relation_crud_and_transitive_impact_analysis():
    first = client.post("/api/v1/requirements", json={"key": "REQ-001", "title": "Giriş"}).json()["id"]
    second = client.post("/api/v1/requirements", json={"key": "REQ-002", "title": "Rapor"}).json()["id"]
    third = client.post("/api/v1/requirements", json={"key": "REQ-003", "title": "Bildirim"}).json()["id"]
    for source, target in ((first, second), (second, third)):
        assert client.post("/api/v1/relations", json={"source_requirement_id": source, "target_requirement_id": target, "relation_type": "depends_on"}).status_code == 201

    impact = client.get("/api/v1/impact-analysis/REQ-001")

    assert impact.status_code == 200
    assert [(item["key"], item["distance"]) for item in impact.json()["affected_requirements"]] == [("REQ-002", 1), ("REQ-003", 2)]
    relation_id = client.get("/api/v1/relations").json()[0]["id"]
    assert client.delete(f"/api/v1/relations/{relation_id}").status_code == 204


def test_core_screens_and_pdf_export_are_available():
    for path in ("/", "/wiegers/scoring", "/traceability/matrix", "/impact-analysis"):
        assert client.get(path).status_code == 200
    pdf = client.get("/api/v1/reports/pdf")
    assert pdf.status_code == 200
    assert pdf.headers["content-type"].startswith("application/pdf")
    assert pdf.content.startswith(b"%PDF")


def test_prioritization_dashboard_links_results_to_traceability_graph():
    response = client.get("/prioritization/dashboard")

    assert response.status_code == 200
    assert "Önceliklendirme sonuçları" in response.text
    assert "/api/v1/prioritization/results" in response.text
    assert "/traceability/graph?highlight=" in response.text


def test_volere_score_rejects_duplicate_criterion_names():
    requirement_id = client.post("/api/v1/requirements", json={"key": "REQ-001", "title": "Kullanıcı girişi"}).json()["id"]
    response = client.put(
        "/api/v1/volere/scores",
        json={
            "requirement_id": requirement_id,
            "criteria": [
                {"name": "Değer", "weight": 50, "score": 8},
                {"name": " değer ", "weight": 50, "score": 6},
            ],
        },
    )
    assert response.status_code == 422


def test_volere_score_rejects_missing_requirement_and_out_of_range_score():
    missing_requirement = client.put(
        "/api/v1/volere/scores",
        json={"requirement_id": 99, "criteria": [{"name": "Değer", "weight": 100, "score": 8}]},
    )
    requirement_id = client.post("/api/v1/requirements", json={"key": "REQ-001", "title": "Kullanıcı girişi"}).json()["id"]
    invalid_score = client.put(
        "/api/v1/volere/scores",
        json={"requirement_id": requirement_id, "criteria": [{"name": "Değer", "weight": 100, "score": 11}]},
    )

    assert missing_requirement.status_code == 404
    assert invalid_score.status_code == 422


def test_ahp_comparison_is_saved_once_per_requirement_pair():
    left_id = client.post("/api/v1/requirements", json={"key": "REQ-001", "title": "Kullanıcı girişi"}).json()["id"]
    right_id = client.post("/api/v1/requirements", json={"key": "REQ-002", "title": "Rapor üretimi"}).json()["id"]

    saved = client.put(
        "/api/v1/ahp/comparisons",
        json={"left_requirement_id": left_id, "right_requirement_id": right_id, "comparison_value": "5"},
    )
    updated_inverse = client.put(
        "/api/v1/ahp/comparisons",
        json={"left_requirement_id": right_id, "right_requirement_id": left_id, "comparison_value": "1/3"},
    )

    assert saved.status_code == 200
    assert updated_inverse.status_code == 200
    assert len(client.get("/api/v1/ahp/comparisons").json()) == 1
    assert updated_inverse.json()["comparison_value"] == "3.00000000"


def test_ahp_comparison_rejects_same_requirement():
    requirement_id = client.post("/api/v1/requirements", json={"key": "REQ-001", "title": "Kullanıcı girişi"}).json()["id"]
    response = client.put(
        "/api/v1/ahp/comparisons",
        json={"left_requirement_id": requirement_id, "right_requirement_id": requirement_id, "comparison_value": "1"},
    )
    assert response.status_code == 422


def test_ahp_comparison_rejects_invalid_scale_for_existing_requirements():
    left_id = client.post("/api/v1/requirements", json={"key": "REQ-001", "title": "Kullanıcı girişi"}).json()["id"]
    right_id = client.post("/api/v1/requirements", json={"key": "REQ-002", "title": "Rapor üretimi"}).json()["id"]

    response = client.put(
        "/api/v1/ahp/comparisons",
        json={"left_requirement_id": left_id, "right_requirement_id": right_id, "comparison_value": "10"},
    )

    assert response.status_code == 422


def test_ahp_comparison_rejects_missing_requirement():
    requirement_id = client.post("/api/v1/requirements", json={"key": "REQ-001", "title": "Kullanıcı girişi"}).json()["id"]
    response = client.put(
        "/api/v1/ahp/comparisons",
        json={"left_requirement_id": requirement_id, "right_requirement_id": 99, "comparison_value": "3"},
    )

    assert response.status_code == 404
