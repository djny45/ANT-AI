import asyncio

from ant_langgraph.integration_pipeline import run_pipeline
from intelligence.ollama_connector import OllamaConnector


def _fake_generate(self, prompt, *args, **kwargs):
    """Deterministic model double compatible with the connector contract."""
    return {
        "response": "test model response",
        "model": "test-double",
        "latency_ms": 1.0,
        "done": True,
    }


def test_run_pipeline_basic(monkeypatch):
    """The unified intelligence boundary works without a live Ollama server."""
    monkeypatch.setenv("ANT_MODEL_PROVIDER", "ollama")
    monkeypatch.setattr(OllamaConnector, "generate", _fake_generate)
    result = asyncio.run(run_pipeline({
        "user_input": "test integration",
        "context": {"trace": True},
        "conversation_id": "basic-integration-test",
    }))

    assert isinstance(result, dict)
    assert result["execution_id"]
    assert result["final_response"]
    assert result["selected_capabilities"] == ["testing"]
    assert result["fast_path"] is True
    assert result["parallel_execution"] is False
    assert result["verification_results"]["status"] == "passed"
    assert result["governance"]["approved"] is True
    assert result["memory_saved"] is True
    assert result["audit_id"]


def test_dynamic_capability_selection(monkeypatch):
    """One request forms only the internal capabilities it needs."""
    monkeypatch.setenv("ANT_MODEL_PROVIDER", "ollama")
    monkeypatch.setattr(OllamaConnector, "generate", _fake_generate)
    result = asyncio.run(run_pipeline({"user_input": "build and test authentication"}))
    assert "coding" in result["selected_capabilities"]
    assert "testing" in result["selected_capabilities"]
    assert "reasoning" not in result["selected_capabilities"]
    assert result["parallel_execution"] is True


def test_memory_lifecycle(monkeypatch):
    """Verified results are stored and available on the next request."""
    monkeypatch.setenv("ANT_MODEL_PROVIDER", "ollama")
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
