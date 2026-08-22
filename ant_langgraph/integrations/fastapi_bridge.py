"""
ANT AI FastAPI -> unified intelligence runtime bridge.

The API exposes one ANT intelligence core. Capabilities are temporary
cognitive pathways formed for the current request; they are not permanent
independent agents.
"""

from typing import Any, Dict

from ant_langgraph.integration_pipeline import run_pipeline


async def process_chat_request(
    message: str,
    user_id: str | None = None,
    conversation_id: str | None = None,
    context: Dict[str, Any] | None = None,
) -> Dict[str, Any]:
    """Execute a user request through the complete ANT runtime boundary."""
    result = await run_pipeline({
        "user_input": message,
        "user_id": user_id,
        "conversation_id": conversation_id,
        "context": context or {},
    })

    return {
        "response": result.get("final_response", ""),
        "capabilities_used": result.get("selected_agents", []),
        "execution_plan": result.get("execution_plan", []),
        "verification": result.get("verification_results", {}),
        "governance": result.get("governance", {}),
        "risk_score": result.get("risk_score", 0),
        "memory_saved": result.get("memory_saved", False),
        "memory_context": result.get("memory_context", {}),
        "audit_id": result.get("audit_id"),
        "latency_ms": result.get("latency_ms", 0.0),
        "errors": result.get("errors", []),
    }
