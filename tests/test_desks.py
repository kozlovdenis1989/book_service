from fastapi.testclient import TestClient
from app.main import app
from app import schemas
import random
import pytest

client = TestClient(app)

@pytest.fixture
def create_desk_data():
    return {
        "name": "Test Desk " + str(random.randint(1, 100)),  
        "seats": 4,
        "location": "Test Location " + str(random.randint(1, 100)),  
    }

@pytest.fixture
def create_desk_with_unique_name():
    return {
        "name": "Unique Desk",
        "seats": 2,
        "location": "Unique Location"
    }

@pytest.fixture(autouse=True)
def clean_db():
    pass

def test_create_desk(create_desk_data):
    response = client.post("/desks/", json=create_desk_data)
    print("Response status code:", response.status_code)
    print("Response data:", response.json())  
    assert response.status_code == 200
    assert response.json()["name"] == create_desk_data["name"]
    assert response.json()["seats"] == create_desk_data["seats"]

def test_create_desk_with_same_name(create_desk_with_unique_name, create_desk_data):
    client.post("/desks/", json=create_desk_data)  
    response = client.post("/desks/", json=create_desk_with_unique_name)  
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
        print("Failed to create desk:", response.status_code, response.json())

def test_delete_nonexistent_desk():
    response = client.delete("/desks/9999") 
    assert response.status_code == 404
    assert response.json()["detail"] == "Desk not found"









