import random
import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.db import SessionLocal
from sqlalchemy.orm import Session
from sqlalchemy import text

client = TestClient(app)

@pytest.fixture(autouse=True)
def clear_db_after_test():
    yield
    db: Session = SessionLocal()
    db.execute(text('TRUNCATE TABLE reservations RESTART IDENTITY CASCADE;'))
    db.execute(text('TRUNCATE TABLE desks RESTART IDENTITY CASCADE;'))
    db.commit()
    db.close()

@pytest.fixture
def create_desk():
    desk_data = {
        "name": "Test Desk " + str(random.randint(1, 1000)),
        "seats": 4,
        "location": "Test Location " + str(random.randint(1, 1000)),
    }
    response = client.post("/desks/", json=desk_data)
    return response.json()

@pytest.fixture
def create_reservation_data(create_desk):
    return {
        "customer_name": "John Doe",
        "desk_id": create_desk["id"],
        "reservation_time": "2023-12-01T12:00:00",
        "duration_minutes": 2,
    }

def test_create_reservation(create_reservation_data):
    response = client.post("/reservations/", json=create_reservation_data)
    assert response.status_code == 200
    assert response.json()["customer_name"] == create_reservation_data["customer_name"]
    assert response.json()["desk_id"] == create_reservation_data["desk_id"]

def test_create_reservation_conflict(create_reservation_data):
    response = client.post("/reservations/", json=create_reservation_data)
    assert response.status_code == 200
    assert 'id' in response.json()

    conflict_response = client.post("/reservations/", json=create_reservation_data)
    assert conflict_response.status_code == 400
    assert "Time slot is already taken" in conflict_response.json()["detail"]

def test_delete_reservation(create_reservation_data):
    create_response = client.post("/reservations/", json=create_reservation_data)
    reservation_id = create_response.json()["id"]

    delete_response = client.delete(f"/reservations/{reservation_id}")
    assert delete_response.status_code == 200
    assert delete_response.json()["message"] == "Reservation deleted"

    get_response = client.get("/reservations/")
    assert all(res['id'] != reservation_id for res in get_response.json())

def test_delete_nonexistent_reservation():
    response = client.delete("/reservations/9999")
    assert response.status_code == 404
    assert response.json()["detail"] == "Reservation not found"