import pytest
from fastapi.testclient import TestClient

try:
    from ANT_X_OS.api import server
except Exception:
    server = None

API_KEY = "test-api-key"


@pytest.fixture()
def client(monkeypatch):
    if not server or getattr(server, "app", None) is None:
        pytest.skip("FastAPI app not available in this environment")
    monkeypatch.setenv("ANT_API_KEY", API_KEY)
    return TestClient(server.app)


def test_execute_endpoint_returns_expected_shape(client):
    resp = client.post(
        "/execute",
        json={"message": "test from fastapi"},
        headers={"X-API-Key": API_KEY},
    )
    assert resp.status_code == 200
    data = resp.json()

    # Two possible shapes: normalized LangGraph output or fallback
    if "final_response" in data:
        # Expected normalized shape from run_pipeline
        assert "selected_agents" in data
        assert "agent_results" in data
        assert data["final_response"] != ""
    else:
        # Fallback shape
        assert data.get("status") == "received"


def test_execute_requires_api_key(client):
    resp = client.post("/execute", json={"message": "no key"})
    assert resp.status_code == 401

    resp = client.post(
        "/execute",
        json={"message": "wrong key"},
        headers={"X-API-Key": "nope"},
    )
    assert resp.status_code == 401


def test_execute_rejects_dangerous_input(client):
    resp = client.post(
        "/execute",
        json={"message": "<script>alert(1)</script>"},
        headers={"X-API-Key": API_KEY},
    )
    assert resp.status_code == 400


def test_skills_status_requires_api_key(client):
    assert client.get("/skills/status").status_code == 401
    resp = client.get("/skills/status", headers={"X-API-Key": API_KEY})
    assert resp.status_code == 200


def test_security_headers_present(client):
    resp = client.post(
        "/execute",
        json={"message": "headers"},
        headers={"X-API-Key": API_KEY},
    )
    assert resp.headers["x-frame-options"] == "DENY"
    assert resp.headers["x-content-type-options"] == "nosniff"
