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
def create_desk_data():
    return {
        "name": "Test Desk " + str(random.randint(1, 1000)),
        "seats": 4,
        "location": "Test Location " + str(random.randint(1, 1000)),
    }

@pytest.fixture
def create_desk_with_unique_name():
    return {
        "name": "Unique Desk",
        "seats": 2,
        "location": "Unique Location"
    }

def test_create_desk(create_desk_data):
    response = client.post("/desks/", json=create_desk_data)
    assert response.status_code == 200
    assert response.json()["name"] == create_desk_data["name"]
    assert response.json()["seats"] == create_desk_data["seats"]

def test_create_desk_with_same_name(create_desk_with_unique_name, create_desk_data):
    client.post("/desks/", json=create_desk_data) 
    response = client.post("/desks/", json=create_desk_data)  
    assert response.status_code == 400
    assert "A desk with this name or location already exists" in response.json()["detail"]

def test_get_desks(create_desk_data):
    client.post("/desks/", json=create_desk_data)
    response = client.get("/desks/")
    assert response.status_code == 200
    assert len(response.json()) > 0

def test_delete_desk(create_desk_data):
    response = client.post("/desks/", json=create_desk_data)
    if response.status_code == 200:
        desk_id = response.json().get("id")
        delete_response = client.delete(f"/desks/{desk_id}")
        assert delete_response.status_code == 200
        assert delete_response.json()["message"] == "Desk deleted"

        get_response = client.get("/desks/")
        assert all(desk['id'] != desk_id for desk in get_response.json())
    else:
        pytest.fail(f"Failed to create desk: {response.status_code}, {response.json()}")

def test_delete_nonexistent_desk():
    response = client.delete("/desks/9999")
    assert response.status_code == 404
    assert response.json()["detail"] == "Desk not found"







