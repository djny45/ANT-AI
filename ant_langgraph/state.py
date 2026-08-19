from dataclasses import dataclass, field
from typing import Any


@dataclass
class AgentState:
    """Mutable state shared by nodes during one workflow execution."""

    user_input: str
    user_context: dict[str, Any] = field(default_factory=dict)
    conversation_id: str | None = None
    request_id: str = ""
    request_timestamp: str = ""
    execution_plan: list[dict[str, Any]] = field(default_factory=list)
    selected_agents: list[str] = field(default_factory=list)
    strategy: str = "PENDING"
    required_capabilities: list[str] = field(default_factory=list)
    confidence: float = 0.0
    intent: str = "PENDING"
    complexity: str = "PENDING"
    capability_selections: list[dict[str, Any]] = field(default_factory=list)
    current_node: str | None = None
    agent_results: list[dict[str, Any]] = field(default_factory=list)
    tool_results: list[dict[str, Any]] = field(default_factory=list)
    memory_context: dict[str, Any] = field(default_factory=dict)
    memory_saved: bool = False
    verification_results: dict[str, Any] = field(default_factory=dict)
    final_response: str | None = None
    audit_metadata: dict[str, Any] = field(default_factory=dict)
    errors: list[str] = field(default_factory=list)
    stage_status: dict[str, str] = field(default_factory=dict)
    recovery_records: list[dict[str, Any]] = field(default_factory=list)
    events: list[dict[str, Any]] = field(default_factory=list)

    def record_result(self, agent: str, result: Any, confidence: float = 0.0) -> None:
        self.agent_results.append({
            "agent": agent,
            "result": result,
            "confidence": max(0.0, min(1.0, confidence)),
        })

    def fail(self, message: str) -> None:
        self.errors.append(message)
