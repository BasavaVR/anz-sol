from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_healthz_endpoint():
    response = client.get("/healthz")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}

def test_info_endpoint_structure():
    response = client.get("/info")
    assert response.status_code == 200
    data = response.json()
    
    required_keys = ["application", "version", "git_commit", "build_timestamp", "environment", "status"]
    for key in required_keys:
        assert key in data
    assert data["status"] == "healthy"