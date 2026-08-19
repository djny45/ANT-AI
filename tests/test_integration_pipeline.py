import asyncio

from ant_langgraph.integration_pipeline import run_pipeline


def test_run_pipeline_basic():
    """Integration test for the LangGraph run_pipeline entrypoint.

    This ensures the FastAPI bridge / callers receive a normalized dict
    with expected keys after executing the default graph.
    """
    state = {"user_input": "test integration", "context": {"trace": True}}
    result = asyncio.run(run_pipeline(state))

    assert isinstance(result, dict)
    # Core output keys expected by FastAPI bridge
    assert "final_response" in result
    assert "selected_agents" in result
    assert "agent_results" in result

    # The default synthesizer provides a non-empty final_response
    assert result["final_response"] != ""
