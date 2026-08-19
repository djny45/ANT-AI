import pytest
from fastapi.testclient import TestClient

try:
    from ANT_X_OS.api import server
except Exception:
    server = None


def test_execute_endpoint_returns_expected_shape():
    if not server or getattr(server, "app", None) is None:
        pytest.skip("FastAPI app not available in this environment")

    client = TestClient(server.app)
    resp = client.post("/execute", json={"message": "test from fastapi"})
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
