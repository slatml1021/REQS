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
