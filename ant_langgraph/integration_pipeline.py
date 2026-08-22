"""ANT AI execution boundary for the unified intelligence graph."""

from dataclasses import dataclass, field
from typing import Any, Dict, List
from uuid import uuid4

from .graph import build_default_graph
from .memory import MemoryAdapter
from .state import AgentState
from governance_engine.governance.approval_flow import ApprovalFlow
from governance_engine.governance.audit_log import AuditLog


@dataclass
class GraphExecutionState:
    user_input: str
    context: Dict[str, Any] = field(default_factory=dict)
    tasks: List[Dict[str, Any]] = field(default_factory=list)
    results: List[Dict[str, Any]] = field(default_factory=list)
    final_response: str = ""
    audit_id: str | None = None


# Lightweight process-local services for the free/open-source prototype.
# Production deployments can replace these through the existing adapter boundaries.
_MEMORY = MemoryAdapter()
_AUDIT = AuditLog()
_GOVERNANCE = ApprovalFlow()


class ANTXOSPipeline:
    """Execution boundary with injectable model, memory, governance and audit services."""

    def __init__(self, router=None, memory=None, audit=None, governance=None):
        self.router = router
        self.memory = memory or _MEMORY
        self.audit = audit or _AUDIT
        self.governance = governance or _GOVERNANCE

    async def execute(self, state: GraphExecutionState) -> GraphExecutionState:
        if not state.audit_id:
            state.audit_id = str(uuid4())
        self.audit.record(
            "graph_execution_started",
            {"execution_id": state.audit_id, "input": state.user_input},
        )
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

    execution_id = str(uuid4())
    _AUDIT.record("request_received", {"execution_id": execution_id})

    state = AgentState(
        user_input=user_input,
        user_context=context,
        conversation_id=conversation_id,
    )

    # Retrieve relevant context before planning.
    state.memory_context = _MEMORY.load(conversation_id)

    graph = build_default_graph()
    state = graph.run(state)

    # Governance is enforced inside the graph immediately before capability execution.
    risk_score = int(state.audit_metadata.get("risk_score", 0))
    governance_approved = bool(state.audit_metadata.get("governance_approved", False))

    # Persist only verified outcomes.
    memory_saved = False
    if conversation_id and state.verification_results.get("status") == "passed":
        _MEMORY.save(conversation_id, {
            "execution_id": execution_id,
            "request": user_input,
            "capabilities": list(state.selected_agents),
            "response": state.final_response or "",
            "verification": state.verification_results,
        })
        memory_saved = True

    _AUDIT.record(
        "graph_execution_completed",
        {
            "execution_id": execution_id,
            "capabilities": list(state.selected_agents),
            "risk_score": risk_score,
            "governance_approved": governance_approved,
            "verification": state.verification_results,
            "memory_saved": memory_saved,
            "errors": list(state.errors),
        },
    )

    return {
        "execution_id": execution_id,
        "final_response": state.final_response or "",
        "selected_agents": state.selected_agents,
        "agent_results": state.agent_results,
        "verification_results": state.verification_results,
        "errors": state.errors,
        "risk_score": risk_score,
        "governance": {
            "approved": governance_approved,
            "reason": state.audit_metadata.get("governance_reason", ""),
        },
        "memory_saved": memory_saved,
        "memory_context": state.memory_context,
        "audit_id": execution_id,
        "audit_events": _AUDIT.history(),
        "execution_plan": state.execution_plan,
        "current_node": state.current_node,
        "latency_ms": state.audit_metadata.get("latency_ms", 0.0),
    }
