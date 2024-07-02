import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_read_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"status": "Running!"}

def test_greetings():
    response = client.get("/api/hello?visitor_name=TestUser")
    assert response.status_code == 200
    data = response.json()
    assert "client_ip" in data
    assert "location" in data
    assert "greeting" in data
    assert data["greeting"].startswith("Hello, TestUser!, the temperature is")

def test_greetings_default_visitor_name():
    response = client.get("/api/hello")
    assert response.status_code == 200
    data = response.json()
    assert "client_ip" in data
    assert "location" in data
    assert "greeting" in data
    assert "Hello, Guest!" in data["greeting"]

def test_cors_headers():
    headers = {
        "Origin": "http://example.com",
        "Access-Control-Request-Method": "GET",
        "Access-Control-Request-Headers": "Content-Type",
    }
    response = client.options("/api/hello",headers=headers)
    assert response.status_code == 200
    assert "access-control-allow-origin" in response.headers
    assert response.headers["access-control-allow-origin"] == "*"

def test_invalid_route():
    response = client.get("/invalid-route")
    assert response.status_code == 404
    assert response.json() == {"detail": "Not Found"}