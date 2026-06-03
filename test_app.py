import pytest

import app as app_module
from app import app


@pytest.fixture
def client():
    app.config["TESTING"] = True
    # Reset the in-memory store before each test for isolation
    app_module.users = [
        {"id": 1, "name": "Alice"},
        {"id": 2, "name": "Bob"},
    ]
    with app.test_client() as client:
        yield client


def test_get_users(client):
    response = client.get("/users")
    assert response.status_code == 200
    assert response.get_json() == [
        {"id": 1, "name": "Alice"},
        {"id": 2, "name": "Bob"},
    ]


def test_get_user(client):
    response = client.get("/users/1")
    assert response.status_code == 200
    assert response.get_json() == {"id": 1, "name": "Alice"}


def test_get_user_not_found(client):
    response = client.get("/users/999")
    assert response.status_code == 404
    assert response.get_json() == {"error": "User not found"}


def test_create_user(client):
    response = client.post("/users", json={"name": "Carol"})
    assert response.status_code == 201
    assert response.get_json() == {"id": 3, "name": "Carol"}
    # Confirm it was added
    assert len(client.get("/users").get_json()) == 3


def test_update_user(client):
    response = client.put("/users/1", json={"name": "Alicia"})
    assert response.status_code == 200
    assert response.get_json() == {"id": 1, "name": "Alicia"}


def test_update_user_not_found(client):
    response = client.put("/users/999", json={"name": "Nobody"})
    assert response.status_code == 404
    assert response.get_json() == {"error": "User not found"}


def test_delete_user(client):
    response = client.delete("/users/1")
    assert response.status_code == 200
    assert response.get_json() == {"message": "User deleted"}
    # Confirm it was removed
    assert client.get("/users/1").status_code == 404


def test_delete_user_not_found(client):
    response = client.delete("/users/999")
    assert response.status_code == 404
    assert response.get_json() == {"error": "User not found"}
