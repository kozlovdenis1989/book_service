from fastapi.testclient import TestClient
from app.main import app
import pytest
import random

client = TestClient(app)

@pytest.fixture
def create_desk():
    """Создает тестовый столик для использования в тестах бронирования."""
    desk_data = {
        "name": "Test Desk " + str(random.randint(1, 100)),
        "seats": 4,
        "location": "Test Location " + str(random.randint(1, 100)),
    }
    response = client.post("/desks/", json=desk_data)
    return response.json()

@pytest.fixture
def create_reservation_data(create_desk):
    """Дает данные для теста создания резервирования."""
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
    # Создаем первую резерву
    response = client.post("/reservations/", json=create_reservation_data)
    assert response.status_code == 200
    assert 'id' in response.json()  

    # Создаем конфликтующую резерву
    conflict_response = client.post("/reservations/", json=create_reservation_data)
    assert conflict_response.status_code == 400
    assert "Time slot is already taken" in conflict_response.json()["detail"]

def test_delete_reservation(create_reservation_data):
    # Сначала создадим резервирование
    create_response = client.post("/reservations/", json=create_reservation_data)
    reservation_id = create_response.json()["id"]
    
    # Теперь удалим резервирование
    delete_response = client.delete(f"/reservations/{reservation_id}")
    assert delete_response.status_code == 200
    assert delete_response.json()["message"] == "Reservation deleted"

    # Проверим, что резервирование было удалено
    get_response = client.get("/reservations/")
    assert all(reservation['id'] != reservation_id for reservation in get_response.json())

def test_delete_nonexistent_reservation():
    # Попытаемся удалить несуществующую резерву
    response = client.delete("/reservations/9999")  
    assert response.status_code == 404
    assert response.json()["detail"] == "Reservation not found"