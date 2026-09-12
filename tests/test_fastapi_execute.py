from fastapi.testclient import TestClient

from api.chat import app


def test_health_endpoint_returns_expected_shape():
    client = TestClient(app)
    response = client.get("/health")

    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"
    assert data["service"] == "ant-ai-api"
    assert data["provider"] == "openrouter"


def test_chat_endpoint_requires_selected_model():
    client = TestClient(app)
    response = client.post("/", json={"message": "test from fastapi", "context": {}})

    assert response.status_code == 400
    assert "No OpenRouter model selected" in response.json()["detail"]
