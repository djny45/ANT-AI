"""
ANT AI FastAPI -> Graph Runtime Bridge

Connects API requests with the LangGraph-style orchestration layer.
Keeps existing backend services isolated behind an integration boundary.
"""

from typing import Any, Dict

from ant_langgraph.integration_pipeline import run_pipeline


async def process_chat_request(
    message: str,
    user_id: str | None = None,
    conversation_id: str | None = None,
    context: Dict[str, Any] | None = None,
) -> Dict[str, Any]:
    """Execute a user request through the ANT AI graph pipeline."""

    state = {
        "user_input": message,
        "user_id": user_id,
        "conversation_id": conversation_id,
        "context": context or {},
        "agent_results": [],
        "memory_context": {},
        "audit_metadata": {},
    }

    result = await run_pipeline(state)

    return {
        "response": result.get("final_response", ""),
        "agents_used": result.get("selected_agents", []),
        "risk_score": result.get("risk_score", 0),
        "memory_saved": result.get("memory_saved", False),
        "audit_id": result.get("audit_id"),
    }
