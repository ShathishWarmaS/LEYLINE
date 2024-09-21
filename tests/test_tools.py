from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_lookup():
    response = client.get("/v1/tools/lookup?domain=example.com")
    assert response.status_code == 200
    assert "ipv4_addresses" in response.json()

def test_validate_ip():
    response = client.post("/v1/tools/validate", json={"ip": "8.8.8.8"})
    assert response.status_code == 200
    assert response.json()["status"] == True

def test_validate_ip_invalid():
    response = client.post("/v1/tools/validate", json={"ip": "999.999.999.999"})
    assert response.status_code == 200
    assert response.json()["status"] == False
