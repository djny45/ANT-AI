import asyncio

from ant_langgraph.integration_pipeline import run_pipeline
from intelligence.ollama_connector import OllamaConnector


def _fake_generate(self, prompt):
    return {
        "response": "test model response",
        "model": "test-double",
        "latency_ms": 1.0,
    }


def test_run_pipeline_basic(monkeypatch):
    """The execution boundary works without a live Ollama server."""
    monkeypatch.setattr(OllamaConnector, "generate", _fake_generate)
    result = asyncio.run(run_pipeline({
        "user_input": "test integration",
        "context": {"trace": True},
        "conversation_id": "basic-integration-test",
    }))

    assert isinstance(result, dict)
    assert result["execution_id"]
    assert result["final_response"]
    assert result["selected_agents"] == ["reasoning"]
    assert result["verification_results"]["status"] == "passed"
    assert result["governance"]["approved"] is True
    assert result["memory_saved"] is True
    assert result["audit_id"]


def test_dynamic_capability_selection(monkeypatch):
    """A single request forms only the capabilities it needs."""
    monkeypatch.setattr(OllamaConnector, "generate", _fake_generate)
    result = asyncio.run(run_pipeline({"user_input": "build and test authentication"}))
    assert "coding" in result["selected_agents"]
    assert "testing" in result["selected_agents"]
    assert "reasoning" not in result["selected_agents"]


def test_memory_lifecycle(monkeypatch):
    """Verified results are stored and available on the next request."""
    monkeypatch.setattr(OllamaConnector, "generate", _fake_generate)
    conversation_id = "integration-memory-test"
    first = asyncio.run(run_pipeline({
        "user_input": "remember this integration test",
        "conversation_id": conversation_id,
    }))
    assert first["memory_saved"] is True

    second = asyncio.run(run_pipeline({
        "user_input": "continue the integration test",
        "conversation_id": conversation_id,
    }))
    assert second["memory_context"]["short_term"]


def test_empty_request_is_rejected():
    result = asyncio.run(run_pipeline({"user_input": "   "}))
    assert result["errors"] == ["empty_request"]
    assert result["verification_results"]["status"] == "failed"
