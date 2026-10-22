
from datetime import date

import models
from conftest import TestingSessionLocal


def test_create_work_order(client, admin_headers):
    # Create equipment in the test database
    db = TestingSessionLocal()

    try:
        equipment = models.Equipment(
            name="Test Generator",
            equipment_type="Generator",
            manufacturer="Caterpillar",
            model="CAT-100",
            serial_number="TEST-GEN-001",
            location="Test Workshop",
            installation_date=date(2025, 1, 10),
            status="active",
            criticality="high",
        )

        db.add(equipment)
        db.commit()
        db.refresh(equipment)

        equipment_id = equipment.id
    finally:
        db.close()

    # Send a request to our FastAPI endpoint
    response = client.post(
        "/work-orders",
        headers=admin_headers,
        json={
            "equipment_id": equipment_id,
            "title": "Inspect cooling system",
            "description": "Check generator temperature",
            "priority": "high",
            "assigned_to": "Test Technician",
        },
    )

    # Check the API response
    assert response.status_code == 201

    data = response.json()

    assert data["equipment_id"] == equipment_id
    assert data["title"] == "Inspect cooling system"
    assert data["status"] == "open"
    assert data["priority"] == "high"


def test_work_order_status_workflow(client, admin_headers):
    db = TestingSessionLocal()

    try:
        equipment = models.Equipment(
            name="Test Pump",
            equipment_type="Pump",
            manufacturer="Grundfos",
            model="CR-100",
            serial_number="TEST-PUMP-001",
            location="Test Workshop",
            installation_date=date(2025, 1, 10),
            status="active",
            criticality="high",
        )

        db.add(equipment)
        db.commit()
        db.refresh(equipment)
        equipment_id = equipment.id
    finally:
        db.close()

    response = client.post(
        "/work-orders",
        headers=admin_headers,
        json={
            "equipment_id": equipment_id,
            "title": "Repair pump",
            "description": "Inspect pump vibration",
            "priority": "high",
        },
    )

    assert response.status_code == 201

    work_order_id = response.json()["id"]

    # Move from open to in_progress
    response = client.patch(
        f"/work-orders/{work_order_id}/status",
        headers=admin_headers,
        json={"status": "in_progress"},
    )

    assert response.status_code == 200
    assert response.json()["status"] == "in_progress"

    # Complete the work order
    response = client.patch(
        f"/work-orders/{work_order_id}/status",
        headers=admin_headers,
        json={"status": "completed"},
    )

    assert response.status_code == 200
    assert response.json()["status"] == "completed"

    completed_at = response.json()["completed_at"]
    assert completed_at is not None

    # Repeating completed must preserve the timestamp
    response = client.patch(
        f"/work-orders/{work_order_id}/status",
        headers=admin_headers,
        json={"status": "completed"},
    )

    assert response.status_code == 200
    assert response.json()["completed_at"] == completed_at

    # Completed work orders cannot be reopened
    response = client.patch(
        f"/work-orders/{work_order_id}/status",
        headers=admin_headers,
        json={"status": "open"},
    )

    assert response.status_code == 409

