from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app, base_url="http://testserver")

def test_root():
    response = client.get("/")
    assert response.status_code == 200, f"Unexpected status code: {response.status_code}, Response: {response.json()}"

def test_health():
    response = client.get("/health")
    assert response.status_code == 200, f"Unexpected status code: {response.status_code}, Response: {response.json()}"
