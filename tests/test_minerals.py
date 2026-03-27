import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.db.base import Base
from app.db.session import get_db
from main import app

TEST_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(TEST_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db


@pytest.fixture(autouse=True)
def setup_db():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


client = TestClient(app)

SAMPLE_MINERAL = {
    "mineral_name": "Cobalt",
    "region_province": "Haut-Katanga",
    "category": "Base Metal",
    "primary_use_industry": "Battery Manufacturing",
    "applications": "Electric Vehicles, Consumer Electronics",
    "mining_status": "Active",
    "year_recorded": 2022,
    "source_system": "GeoData_Africa_API",
    "is_verified": True,
    "confidence_score": 0.95,
    "data_quality_flag": "VERIFIED"
}


def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json()["status"] == "running"


def test_list_minerals_empty():
    response = client.get("/api/v1/minerals/")
    assert response.status_code == 200
    assert response.json() == []


def test_create_mineral():
    response = client.post("/api/v1/minerals/", json=SAMPLE_MINERAL)
    assert response.status_code == 201
    data = response.json()
    assert data["mineral_name"] == "Cobalt"
    assert data["region_province"] == "Haut-Katanga"
    assert data["is_active"] == True
    assert "record_id" in data


def test_get_mineral_by_id():
    created = client.post("/api/v1/minerals/", json=SAMPLE_MINERAL).json()
    record_id = created["record_id"]
    response = client.get(f"/api/v1/minerals/{record_id}")
    assert response.status_code == 200
    assert response.json()["record_id"] == record_id


def test_get_mineral_not_found():
    response = client.get("/api/v1/minerals/00000000-0000-0000-0000-000000000000")
    assert response.status_code == 404
    assert response.json()["detail"] == "Mineral not found"


def test_list_minerals_with_filter():
    client.post("/api/v1/minerals/", json=SAMPLE_MINERAL)
    response = client.get("/api/v1/minerals/?region=Haut-Katanga")
    assert response.status_code == 200
    assert len(response.json()) == 1
    response = client.get("/api/v1/minerals/?region=Nonexistent")
    assert response.status_code == 200
    assert response.json() == []


def test_update_mineral():
    created = client.post("/api/v1/minerals/", json=SAMPLE_MINERAL).json()
    record_id = created["record_id"]
    response = client.patch(
        f"/api/v1/minerals/{record_id}",
        json={"mineral_name": "Cobalt Updated", "confidence_score": 0.99}
    )
    assert response.status_code == 200
    assert response.json()["mineral_name"] == "Cobalt Updated"
    assert response.json()["confidence_score"] == 0.99


def test_update_mineral_not_found():
    response = client.patch(
        "/api/v1/minerals/00000000-0000-0000-0000-000000000000",
        json={"mineral_name": "Ghost"}
    )
    assert response.status_code == 404


def test_soft_delete_mineral():
    created = client.post("/api/v1/minerals/", json=SAMPLE_MINERAL).json()
    record_id = created["record_id"]
    response = client.delete(f"/api/v1/minerals/{record_id}")
    assert response.status_code == 204
    response = client.get(f"/api/v1/minerals/{record_id}")
    assert response.status_code == 404


def test_delete_mineral_not_found():
    response = client.delete("/api/v1/minerals/00000000-0000-0000-0000-000000000000")
    assert response.status_code == 404


def test_confidence_score_validation():
    invalid_payload = {**SAMPLE_MINERAL, "confidence_score": 1.5}
    response = client.post("/api/v1/minerals/", json=invalid_payload)
    assert response.status_code == 422


def test_pagination():
    for i in range(5):
        client.post("/api/v1/minerals/", json={**SAMPLE_MINERAL, "mineral_name": f"Mineral {i}"})
    response = client.get("/api/v1/minerals/?limit=2&skip=0")
    assert len(response.json()) == 2
    response = client.get("/api/v1/minerals/?limit=2&skip=2")
    assert len(response.json()) == 2