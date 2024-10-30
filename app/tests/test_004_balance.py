import pytest
from fastapi.testclient import TestClient
from ..config.app_config import app_config 
from ..main import app

client = TestClient(app)
token = app_config["TEST_TOKEN"]

def test_create_balance():
    response = client.get('/balance', headers={"Authorization": token})
    assert response.status_code == 200
    assert 'data' in response.json()
    assert 'amount' in response.json()['data']
    