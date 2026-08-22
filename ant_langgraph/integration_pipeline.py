"""ANT AI execution boundary for the unified intelligence graph."""

from dataclasses import dataclass, field
from typing import Any, Dict, List

from .graph import build_default_graph
from .memory import MemoryAdapter
from .state import AgentState
from governance_engine.governance.approval_flow import ApprovalFlow


@dataclass
class GraphExecutionState:
    user_input: str
    context: Dict[str, Any] = field(default_factory=dict)
    tasks: List[Dict[str, Any]] = field(default_factory=list)
    results: List[Dict[str, Any]] = field(default_factory=list)
    final_response: str = ""
    audit_id: str | None = None


class ANTXOSPipeline:
    """Execution boundary with injectable model, memory, governance and audit services."""

    def __init__(self, router=None, memory=None, audit=None, governance=None):
        self.router = router
        self.memory = memory or MemoryAdapter()
        self.audit = audit
        self.governance = governance or ApprovalFlow()

    async def execute(self, state: GraphExecutionState) -> GraphExecutionState:
        if self.audit:
            event = {"event": "graph_execution_started", "input": state.user_input}
            result = self.audit.log(event)
            if hasattr(result, "__await__"):
                await result
        return state


async def run_pipeline(request_state: Dict[str, Any]) -> Dict[str, Any]:
    """Run a request through the unified ANT capability workflow."""
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

    # Retrieve relevant short-term context before planning.
    memory = MemoryAdapter()
    state.memory_context = memory.load(conversation_id)

    graph = build_default_graph()
    state = graph.run(state)

    # Apply the existing governance policy to the formed capability set.
    risk_score = min(100, len(state.selected_agents) * 15)
    if any(capability in {"security", "coding"} for capability in state.selected_agents):
        risk_score = min(100, risk_score + 10)
    decision = ApprovalFlow().evaluate(risk_score)
    state.audit_metadata.update({
        "risk_score": risk_score,
        "governance_approved": decision.approved,
        "governance_reason": decision.reason,
    })
    if not decision.approved:
        state.fail(decision.reason)
        state.final_response = "ANT blocked this execution under the active governance policy."

    # Persist the verified execution outcome into short-term memory.
    memory_saved = False
    if conversation_id and state.verification_results.get("status") == "passed":
        memory.save(conversation_id, {
            "request": user_input,
            "capabilities": list(state.selected_agents),
            "response": state.final_response or "",
            "verification": state.verification_results,
        })
        memory_saved = True

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
        "governance": {
            "approved": state.audit_metadata.get("governance_approved", False),
            "reason": state.audit_metadata.get("governance_reason", ""),
        },
        "memory_saved": memory_saved,
        "memory_context": state.memory_context,
        "audit_id": execution.audit_id,
        "execution_plan": state.execution_plan,
        "current_node": state.current_node,
        "latency_ms": state.audit_metadata.get("latency_ms", 0.0),
    }
