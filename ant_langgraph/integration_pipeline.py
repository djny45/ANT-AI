"""ANT AI execution boundary for the unified intelligence graph."""

from dataclasses import dataclass, field
from typing import Any, Dict, List

from .graph import build_default_graph
from .state import AgentState


@dataclass
class GraphExecutionState:
    user_input: str
    context: Dict[str, Any] = field(default_factory=dict)
    tasks: List[Dict[str, Any]] = field(default_factory=list)
    results: List[Dict[str, Any]] = field(default_factory=list)
    final_response: str = ""
    audit_id: str | None = None


class ANTXOSPipeline:
    """Execution boundary that keeps optional services injectable."""

    def __init__(self, router=None, memory=None, audit=None):
        self.router = router
        self.memory = memory
        self.audit = audit

    async def execute(self, state: GraphExecutionState) -> GraphExecutionState:
        if self.audit:
            event = {"event": "graph_execution_started", "input": state.user_input}
            result = self.audit.log(event)
            if hasattr(result, "__await__"):
                await result
        return state


async def run_pipeline(request_state: Dict[str, Any]) -> Dict[str, Any]:
    """Run a request through the unified ANT capability workflow.

    The function accepts ``message`` or ``user_input`` and returns a stable
    dictionary for API consumers. Model, memory, and audit adapters remain
    optional so the graph can run locally without paid services.
    """
    user_input = (request_state.get("user_input") or request_state.get("message") or "").strip()
    context = request_state.get("context") or request_state.get("user_context") or {}
    conversation_id = request_state.get("conversation_id")

    if not user_input:
        return {
            "final_response": "A non-empty request is required.",
            "selected_agents": [],
            "agent_results": [],
            "verification_results": {"status": "failed", "reason": "empty_request"},
            "errors": ["empty_request"],
            "risk_score": 0,
            "memory_saved": False,
            "audit_id": None,
        }

    state = AgentState(
        user_input=user_input,
        user_context=context,
        conversation_id=conversation_id,
    )

    graph = build_default_graph()
    state = graph.run(state)

    execution = GraphExecutionState(
        user_input=user_input,
        context=context,
        tasks=state.execution_plan,
        results=state.agent_results,
        final_response=state.final_response or "",
    )
    await ANTXOSPipeline().execute(execution)

    return {
        "final_response": state.final_response or "",
        "selected_agents": state.selected_agents,
        "agent_results": state.agent_results,
        "verification_results": state.verification_results,
        "errors": state.errors,
        "risk_score": state.audit_metadata.get("risk_score", 0),
        "memory_saved": False,
        "audit_id": execution.audit_id,
        "execution_plan": state.execution_plan,
        "current_node": state.current_node,
    }
