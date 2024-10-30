import pytest
from fastapi.testclient import TestClient
from ..config.app_config import app_config 
from ..main import app

client = TestClient(app)
token = app_config["TEST_TOKEN"]

def test_create_category():
 response = client.post('/category', json={"name": "category 1"}, headers={"Authorization": token})
 assert response.status_code == 201
 assert response.json()['details'] == "category created successfully"
 response = client.post('/category', json={"name": "category 1"}, headers={"Authorization": token})
 assert response.status_code == 400
 assert response.json()['details'] == "category already exists"

def test_update_category():
    response = client.post('/category' , json={"name": "category 2"}, headers={"Authorization": token})
    assert response.status_code == 201
    assert response.json()['details'] == "category created successfully"
    response = client.put('/category/2', params={"category_id": 2}, json={"name": "category 2 updated"}, headers={"Authorization": token})
    assert response.status_code == 200
    assert response.json()['details'] == "category updated successfully"
    response = client.put('/category/2', params={"category_id": 2} , json={"name": "category 2 updated"}, headers={"Authorization": token})
    assert response.status_code == 200
    assert response.json()['details'] == "category updated successfully"

def test_get_categories():
    response = client.get('/category', headers={"Authorization": token})
    assert response.status_code == 200
    assert len(response.json()['data']) > 0

def test_get_category():
    response = client.get('/category/1', params={"category_id": 1}, headers={"Authorization": token})
    assert response.status_code == 200
    assert response.json()['name'] == "category 1"
    response = client.get('/category/2', params={"category_id": 2}, headers={"Authorization": token})
    assert response.status_code == 200
    assert response.json()['name'] == "category 2 updated"
    response = client.get('/category/3', params={"category_id": 3}, headers={"Authorization": token})
    assert response.status_code == 404
    assert response.json()['details'] == "category not found"
    
