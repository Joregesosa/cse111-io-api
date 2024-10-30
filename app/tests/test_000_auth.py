import pytest
from fastapi.testclient import TestClient
from ..main import app
from ..DB.sqlite_config import create_database

client = TestClient(app)
new_user = { "name": "test", "email": "test@example.com", "password": "123456"}

def test_register():
    
    create_database()
    response = client.post(  "/auth/register", json=new_user)
    assert response.status_code == 201
    assert response.json()["details"] == "user created successfully"

def test_login():
    response = client.post(  "/auth/login", json={"email": new_user["email"], "password": new_user["password"]})
    assert response.status_code == 200
    assert "token" in response.json()
    assert "user" in response.json()
    assert response.json()["user"]["email"] == new_user["email"]
    assert response.json()["user"]["name"] == new_user["name"]

def test_me():
    response = client.post(  "/auth/login", json={"email": new_user["email"], "password": new_user["password"]})
    token = response.json()["token"]
    response = client.get(  "/auth/me", headers={"Authorization": token})
    assert response.status_code == 200
    assert "user" in response.json()
    assert response.json()["user"]["email"] == new_user["email"]
    assert response.json()["user"]["name"] == new_user["name"]

def test_update_user():
    response = client.post("/auth/login", json={"email": new_user["email"], "password": new_user["password"]})
    token = response.json()["token"]
    print(token)
    response = client.post("/auth/update", headers={"Authorization": token}, json={"name": "test2"})
    print(response.json())
    assert response.status_code == 200
    assert response.json()["details"] == "user updated successfully"

def test_change_password():
    response = client.post("/auth/login", json={"email": new_user["email"], "password": new_user["password"]})
    token = response.json()["token"]
    response = client.post("/auth/change-password", headers={"Authorization": token}, json={"oldpassword": new_user["password"], "newpassword": "1234567"})
    assert response.status_code == 200
    assert response.json()["details"] == "password updated successfully"
    response = client.post("/auth/change-password", headers={"Authorization": token},json={"oldpassword": "123456", "newpassword": new_user["password"]})
    assert response.status_code == 400 
    assert response.json()["details"] == "old password is incorrect"
    
    
    
