import pytest
from fastapi.testclient import TestClient
from ..config.app_config import app_config 
from ..main import app

client = TestClient(app)
token = app_config["TEST_TOKEN"]

def test_create_income():
    response = client.post('/income', json={"amount": 1000, "description": "income 1"}, headers={"Authorization": token})
    assert response.status_code == 201
    assert response.json()['details'] == "income created successfully"
    response = client.post('/income', json={"amount": 1200, "description": "income 2"}, headers={"Authorization": token})
    assert response.status_code == 201
    assert response.json()['details'] == "income created successfully"
    
def test_update_income():
    response = client.put('/income/1', params={"income_id": 1}, json={"amount": 2000, "description": "income 1 updated"}, headers={"Authorization": token})
    assert response.status_code == 200
    assert response.json()['details'] == "income updated successfully"
    response = client.put('/income/2', params={"income_id": 2}, json={"amount": 2200, "description": "income 2 updated"}, headers={"Authorization": token})
    assert response.status_code == 200
    assert response.json()['details'] == "income updated successfully"

def test_get_incomes():
    response = client.get('/income', headers={"Authorization": token})
    assert response.status_code == 200
    assert 'data' in response.json()
    assert len(response.json()['data']) == 2
    
def test_get_income():
    response = client.get('/income/1', params={"income_id": 1}, headers={"Authorization": token})
    assert response.status_code == 200
    assert response.json()['amount'] == 2000
    assert response.json()['description'] == "income 1 updated"
    response = client.get('/income/2', params={"income_id": 2}, headers={"Authorization": token})
    assert response.status_code == 200
    assert response.json()['amount'] == 2200
    assert response.json()['description'] == "income 2 updated"
    response = client.get('/income/3', params={"income_id": 3}, headers={"Authorization": token})
    assert response.status_code == 404
    assert response.json()['details'] == "income not found"
    
