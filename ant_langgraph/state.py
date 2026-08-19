from dataclasses import dataclass, field
from typing import Any, Dict, List


@dataclass
class AgentState:
    """Mutable state shared by nodes during one workflow execution."""

    user_input: str
    user_context: Dict[str, Any] = field(default_factory=dict)
    conversation_id: str | None = None
    request_id: str = ""
    request_timestamp: str = ""
    execution_plan: List[Dict[str, Any]] = field(default_factory=list)
    selected_agents: List[str] = field(default_factory=list)
    strategy: str = "PENDING"
    required_capabilities: List[str] = field(default_factory=list)
    confidence: float = 0.0
    intent: str = "PENDING"
    complexity: str = "PENDING"
    capability_selections: List[Dict[str, Any]] = field(default_factory=list)
    current_node: str | None = None
    agent_results: List[Dict[str, Any]] = field(default_factory=list)
    tool_results: List[Dict[str, Any]] = field(default_factory=list)
    memory_context: Dict[str, Any] = field(default_factory=dict)
    memory_saved: bool = False
    verification_results: Dict[str, Any] = field(default_factory=dict)
    final_response: str | None = None
    audit_metadata: Dict[str, Any] = field(default_factory=dict)
    errors: List[str] = field(default_factory=list)
    stage_status: Dict[str, str] = field(default_factory=dict)
    recovery_records: List[Dict[str, Any]] = field(default_factory=list)
    events: List[Dict[str, Any]] = field(default_factory=list)

    def record_result(self, agent: str, result: Any, confidence: float = 0.0) -> None:
        self.agent_results.append({
            "agent": agent,
            "result": result,
            "confidence": max(0.0, min(1.0, confidence)),
        })

    def fail(self, message: str) -> None:
        self.errors.append(message)
