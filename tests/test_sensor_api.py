
import models
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from auth_dependencies import get_current_user

from main import app
from database import get_db
from models import Base


# Create an isolated in-memory test database
SQLALCHEMY_TEST_DATABASE_URL = "sqlite://"

engine = create_engine(
    SQLALCHEMY_TEST_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)

TestingSessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)


# Create a test user without storing real credentials
test_user = models.User(
    id=1,
    email="sensor-test@example.com",
    role="admin",
    is_active=True,
)


def override_test_user():
    return test_user





@pytest.fixture
def client():
    Base.metadata.create_all(bind=engine)

    def override_get_db():
        db = TestingSessionLocal()
        try:
            yield db
        finally:
            db.close()

    app.dependency_overrides[get_db] = override_get_db
    app.dependency_overrides[get_current_user] = override_test_user

    try:
        with TestClient(app) as test_client:
            yield test_client
    finally:
        app.dependency_overrides.clear()
        Base.metadata.drop_all(bind=engine)

def test_sensor_history_equipment_not_found(client):
    response = client.get(
        "/sensors/equipment/99999/readings"
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Equipment not found"

    
def test_create_sensor_reading_equipment_not_found(client):
    payload = {
        "equipment_id": 99999,
        "temperature": 75.5,
        "vibration": 2.3,
        "pressure": 5.8,
        "operating_hours": 1200
    }

    response = client.post(
        "/sensors/readings",
        json=payload
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Equipment not found"


def test_create_sensor_reading_success(client):
    from datetime import date
    import models

    # Create equipment in the test database

    db = TestingSessionLocal()

    try:
        equipment = models.Equipment(
            name="Test Generator",
            equipment_type="Generator",
            manufacturer="Caterpillar",
            model="CAT-100",
            serial_number="TEST-GEN-001",
            location="Test Facility",
            installation_date=date(2024, 1, 15),
            criticality="high"
        )

        db.add(equipment)
        db.commit()
        db.refresh(equipment)

        equipment_id = equipment.id

    finally:
        db.close()

    # Submit a sensor reading through the API
    payload = {
        "equipment_id": equipment_id,
        "temperature": 85.5,
        "vibration": 3.5,
        "pressure": 6.2,
        "operating_hours": 1250
    }

    response = client.post(
        "/sensors/readings",
        json=payload
    )

    assert response.status_code == 201

    data = response.json()

    assert data["equipment_id"] == equipment_id
    assert data["temperature"] == 85.5
    assert data["vibration"] == 3.5
    assert data["pressure"] == 6.2
    assert data["id"] > 0
    assert "recorded_at" in data







