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
