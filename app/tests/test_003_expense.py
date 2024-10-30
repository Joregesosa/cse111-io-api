import pytest
from fastapi.testclient import TestClient
from ..config.app_config import app_config 
from ..main import app

client = TestClient(app)
token = app_config["TEST_TOKEN"]

def test_create_expense():
    response = client.post('/expense', json={"amount": 1000, "description": "expense 1", "category_id": 1}, headers={"Authorization": token})
    assert response.status_code == 201 
    print(response.status_code)
    assert response.json()['details'] == "expense created successfully"


def test_update_expense():
    response = client.put('/expense/1', params={"expense_id": 1}, json={"amount": 2000, "description": "expense 1 updated", "category_id": 1}, headers={"Authorization": token})
    assert response.status_code == 200
    assert response.json()['details'] == "expense updated successfully"


def test_get_expenses():
    response = client.get('/expense', headers={"Authorization": token})
    assert response.status_code == 200
    assert 'data' in response.json()
    assert 'amount' in response.json()['data'][0]
    assert 'description' in response.json()['data'][0]

def test_get_expense():
    response = client.get('/expense/1', params={"expense_id": 1}, headers={"Authorization": token})
    assert response.status_code == 200
    assert response.json()['data']['amount'] == 2000
    assert response.json()['data']['description'] == "expense 1 updated"
    response = client.get('/expense/2', params={"expense_id": 2}, headers={"Authorization": token})
    assert response.status_code == 404
    assert response.json()['details'] == "expense not found"

