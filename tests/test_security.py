from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_security_headers():
    response = client.get("/")
    assert response.status_code == 200
    assert response.headers["X-Content-Type-Options"] == "nosniff"
    assert response.headers["X-Frame-Options"] == "DENY"
    assert "Strict-Transport-Security" in response.headers
    assert response.headers["Content-Security-Policy"] == "default-src 'self';"
    assert response.headers["Referrer-Policy"] == "no-referrer"

def test_cors():
    response = client.options("/v1/tools/lookup", headers={"Origin": "https://yourdomain.com"})
    assert response.status_code == 200
    assert response.headers["access-control-allow-origin"] == "https://yourdomain.com"
