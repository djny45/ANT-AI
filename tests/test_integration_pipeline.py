import asyncio

from ant_langgraph.integration_pipeline import run_pipeline


def test_run_pipeline_basic():
    """The execution boundary returns a normalized result."""
    state = {"user_input": "test integration", "context": {"trace": True}}
    result = asyncio.run(run_pipeline(state))

    assert isinstance(result, dict)
    assert result["execution_id"]
    assert "final_response" in result
    assert "selected_agents" in result
    assert "agent_results" in result
    assert "verification_results" in result
    assert "governance" in result
    assert "audit_id" in result


def test_dynamic_capability_selection():
    """A single request forms only the capabilities it needs."""
    result = asyncio.run(run_pipeline({"user_input": "build and test authentication"}))
    assert "coding" in result["selected_agents"]
    assert "testing" in result["selected_agents"]
    assert "reasoning" not in result["selected_agents"]


def test_memory_lifecycle():
    """Verified results are stored and available on the next conversation request."""
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
