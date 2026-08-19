"""ANT AI LangGraph-style integration pipeline."""

from typing import Any, Dict

from .graph import build_default_graph
from .state import AgentState


async def run_pipeline(request_state: Dict[str, Any]) -> Dict[str, Any]:
    """
    Execute a user request through a LangGraph pipeline and return a plain dict
    compatible with FastAPI bridge consumers.

    Expected input (minimal): {"user_input": "...", "context": {...}}
    Returns a dict containing at least: final_response, selected_agents, agent_results.
    """

    # Normalize incoming state
    user_input = request_state.get("user_input") or request_state.get("message") or ""
    conversation_id = request_state.get("conversation_id")
    context = request_state.get("context") or {}

    # Create AgentState for graph execution
    agent_state = AgentState(
        user_input=user_input,
        user_context=context,
        conversation_id=conversation_id,
    )

    # Build and run the default graph. Graph.run is synchronous.
    graph = build_default_graph()
    agent_state = graph.run(agent_state, start="planner")

    # Convert results to plain dict
    out: Dict[str, Any] = {
        "final_response": agent_state.final_response or "",
        "selected_agents": agent_state.selected_agents,
        "agent_results": agent_state.agent_results,
        "verification_results": agent_state.verification_results,
        "errors": agent_state.errors,
        "risk_score": getattr(agent_state, "risk_score", 0),
        "memory_saved": agent_state.memory_saved,
        "audit_id": agent_state.audit_metadata.get("audit_id"),
        "memory_context": agent_state.memory_context,
        "execution_plan": agent_state.execution_plan,
    }

    return out
