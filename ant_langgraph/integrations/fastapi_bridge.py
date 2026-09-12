"""
ANT AI FastAPI -> NOVA Core intelligence runtime bridge.

NOVA Core is the runtime contract used by ANT for hybrid agent planning,
memory, tools, and model-provider execution. ANT remains the control plane
for governance, swarm capabilities, audit, and the user-facing API profile.
"""

from typing import Any, Dict

from ant_langgraph.integration_pipeline import run_pipeline


async def process_chat_request(message: str, user_id: str | None = None, conversation_id: str | None = None, context: Dict[str, Any] | None = None) -> Dict[str, Any]:
    """Execute a user request through the ANT -> NOVA Core runtime boundary."""
    runtime_context = dict(context or {})
    runtime_context.setdefault("runtime", "nova-core")

    result = await run_pipeline({
        "user_input": message,
        "user_id": user_id,
        "conversation_id": conversation_id,
        "context": runtime_context,
    })

    return {
        "response": result.get("final_response", ""),
        "runtime": runtime_context.get("runtime", "nova-core"),
        "capabilities_used": result.get("selected_capabilities", []),
        "execution_plan": result.get("execution_plan", []),
        "verification": result.get("verification_results", {}),
        "governance": result.get("governance", {}),
        "risk_score": result.get("risk_score", 0),
        "memory_saved": result.get("memory_saved", False),
        "memory_context": result.get("memory_context", {}),
        "audit_id": result.get("audit_id"),
        "latency_ms": result.get("latency_ms", 0.0),
        "fast_path": result.get("fast_path", False),
        "parallel_execution": result.get("parallel_execution", False),
        "model_provider": result.get("model_provider", ""),
        "model": result.get("model", ""),
        "errors": result.get("errors", []),
    }
