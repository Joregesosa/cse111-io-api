import pytest
from fastapi.testclient import TestClient
from .main import app

client = TestClient(app)

def test_index():
    response = client.get("/category/")
    assert response.status_code == 401
    
def test_show():
    response = client.get("/category/1")
    assert response.status_code == 401

def test_store():
    response = client.post("/category/")
    assert response.status_code == 401

def test_update():
    response = client.put("/category/1")
    assert response.status_code == 401

def test_destroy():
    response = client.delete("/category/1")
    assert response.status_code == 401
