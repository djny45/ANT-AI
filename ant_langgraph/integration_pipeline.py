"""ANT AI LangGraph-style integration pipeline."""

import os
from typing import Any

from .graph import build_default_graph
from .memory import MemoryAdapter, SQLAlchemyMemoryBackend
from .state import AgentState


async def run_pipeline(request_state: dict[str, Any]) -> dict[str, Any]:
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
    database_url = os.environ.get("ANT_MEMORY_DATABASE_URL")
    memory = (
        MemoryAdapter(SQLAlchemyMemoryBackend(database_url))
        if database_url
        else None
    )
    graph = build_default_graph(memory=memory)
    agent_state = graph.run(agent_state, start="planner")

    def stage_recovery(stage: str) -> list[dict[str, Any]]:
        return [
            record
            for record in agent_state.recovery_records
            if record.get("stage") == stage
        ]

    def stage_status(stage: str) -> str:
        return agent_state.stage_status.get(stage, "completed")

    def stage_event(stage: str) -> dict[str, Any]:
        return next(
            event
            for event in agent_state.events
            if event.get("name") == stage
        )

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
            "event": stage_event("planner"),
            "plan": list(agent_state.execution_plan),
            "strategy": agent_state.strategy,
            "required_capabilities": list(agent_state.required_capabilities),
            "confidence": agent_state.confidence,
            "recovery": stage_recovery("planner"),
        },
        "capability": {
            "status": stage_status("capability"),
            "event": stage_event("capability"),
            "selections": list(agent_state.capability_selections),
            "plan": list(agent_state.execution_plan),
            "recovery": stage_recovery("capability"),
        },
        "execution": {
            "status": stage_status("executor"),
            "event": stage_event("executor"),
            "results": list(agent_state.agent_results),
            "recovery": stage_recovery("executor"),
        },
        "verification": {
            "status": stage_status("verifier"),
            "event": stage_event("verifier"),
            "result": dict(agent_state.verification_results),
            "recovery": stage_recovery("verifier"),
        },
        "memory": {
            "status": stage_status("memory"),
            "event": stage_event("memory"),
            "saved": agent_state.memory_saved,
            "context": dict(agent_state.memory_context),
            "recovery": stage_recovery("memory"),
        },
        "audit": {
            "status": stage_status("audit"),
            "event": stage_event("audit"),
            "metadata": dict(agent_state.audit_metadata),
            "recovery": stage_recovery("audit"),
        },
        "response": {
            "status": stage_status("synthesizer"),
            "event": stage_event("synthesizer"),
            "final_response": agent_state.final_response or "",
            "recovery": stage_recovery("synthesizer"),
        },
    }

    # Convert results to plain dict
    out: dict[str, Any] = {
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
        "events": list(agent_state.events),
        **trace,
    }

    return out
