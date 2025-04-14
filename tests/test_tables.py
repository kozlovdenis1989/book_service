from fastapi.testclient import TestClient
from app.main import app
from app import schemas
import random
import pytest

client = TestClient(app)

@pytest.fixture
def create_table_data():
    return {
        "name": "Test Table " + str(random.randint(1, 100)),  
        "seats": 4,
        "location": "Test Location " + str(random.randint(1, 100)),  
    }

@pytest.fixture
def create_table_with_unique_name():
    return {
        "name": "Unique Table",
        "seats": 2,
        "location": "Unique Location"
    }

@pytest.fixture(autouse=True)
def clean_db():
    # Удаляем все столики из базы данных перед тестами
    client.delete("/tables/")  

def test_create_table(create_table_data):
    response = client.post("/tables/", json=create_table_data)
    print("Response status code:", response.status_code)
    print("Response data:", response.json())  
    assert response.status_code == 200
    assert response.json()["name"] == create_table_data["name"]
    assert response.json()["seats"] == create_table_data["seats"]

def test_create_table_with_same_name(create_table_with_unique_name, create_table_data):
    client.post("/tables/", json=create_table_data)  # создаем первый столик
    response = client.post("/tables/", json=create_table_with_unique_name)  # создаем второй столик с уникальным именем
    assert response.status_code == 400
    assert "A table with this name or location already exists" in response.json()["detail"]

def test_get_tables(create_table_data):
    client.post("/tables/", json=create_table_data)  # создайте столик для теста
    response = client.get("/tables/")
    assert response.status_code == 200
    assert len(response.json()) > 0  

def test_delete_table(create_table_data):
    response = client.post("/tables/", json=create_table_data)
    if response.status_code == 200:
        table_id = response.json().get("id")
        delete_response = client.delete(f"/tables/{table_id}")
        assert delete_response.status_code == 200
        assert delete_response.json()["message"] == "Table deleted"

       
        get_response = client.get("/tables/")
        assert all(table['id'] != table_id for table in get_response.json())
    else:
        print("Failed to create table:", response.status_code, response.json())

def test_delete_nonexistent_table():
    response = client.delete("/tables/9999")  # Предполагаем, что такого столика нет
    assert response.status_code == 404
    assert response.json()["detail"] == "Table not found"