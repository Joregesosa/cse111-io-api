import pytest
from .config.app_config import  app_config
from fastapi.testclient import TestClient
from .main import app
from .DB.sqlite_config import create_database

client = TestClient(app)
token = app_config["TEST_TOKEN"]


def test_index():
    response = client.get("/users", headers={"Authorization": token})
    assert response.status_code == 200
    assert response.json() == []

def test_show():
    response = client.get("/users/2",params={"user_id": 2}, headers={"Authorization": token})
    assert response.json().get('status_code') == 404
    assert response.json().get('detail') == "User not found"

def test_store():
    response = client.post("/users", json={"name": "test", "email": "test@mail.com", "password": "test"}, headers={"Authorization": token})
    assert response.status_code == 201
    assert response.json().get('message') == "user created successfully"
    
def test_update():
    response = client.put("/users/1", params={"user_id": 1} ,  json={"name": "testing"}, headers={"Authorization": token})
    assert response.status_code == 200
    assert response.json().get('message') == "user updated successfully"

 
