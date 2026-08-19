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
    request_id = request_state.get("request_id") or ""

    # Create AgentState for graph execution
    agent_state = AgentState(
        user_input=user_input,
        user_context=context,
        conversation_id=conversation_id,
        request_id=request_id,
    )

    # Build and run the default graph. Graph.run is synchronous.
    graph = build_default_graph()
    agent_state = graph.run(agent_state, start="planner")

    def stage_recovery(stage: str) -> list[Dict[str, Any]]:
        return [
            record
            for record in agent_state.recovery_records
            if record.get("stage") == stage
        ]

    def stage_status(stage: str) -> str:
        return agent_state.stage_status.get(stage, "completed")

    trace = {
        "request": {
            "status": "completed",
            "request_id": agent_state.request_id,
            "timestamp": agent_state.request_timestamp,
            "input": agent_state.user_input,
            "conversation_id": agent_state.conversation_id,
            "intent": agent_state.intent,
            "complexity": agent_state.complexity,
            "recovery": stage_recovery("planner"),
        },
        "plan": {
            "status": stage_status("planner"),
            "plan": list(agent_state.execution_plan),
            "strategy": agent_state.strategy,
            "required_capabilities": list(agent_state.required_capabilities),
            "confidence": agent_state.confidence,
            "recovery": stage_recovery("planner"),
        },
        "capability": {
            "status": stage_status("capability"),
            "selections": list(agent_state.capability_selections),
            "plan": list(agent_state.execution_plan),
            "recovery": stage_recovery("capability"),
        },
        "execution": {
            "status": stage_status("executor"),
            "results": list(agent_state.agent_results),
            "recovery": stage_recovery("executor"),
        },
        "verification": {
            "status": stage_status("verifier"),
            "result": dict(agent_state.verification_results),
            "recovery": stage_recovery("verifier"),
        },
        "memory": {
            "status": stage_status("memory"),
            "saved": agent_state.memory_saved,
            "context": dict(agent_state.memory_context),
            "recovery": stage_recovery("memory"),
        },
        "audit": {
            "status": stage_status("audit"),
            "metadata": dict(agent_state.audit_metadata),
            "recovery": stage_recovery("audit"),
        },
        "response": {
            "status": stage_status("synthesizer"),
            "final_response": agent_state.final_response or "",
            "recovery": stage_recovery("synthesizer"),
        },
    }

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
        **trace,
    }

    return out
