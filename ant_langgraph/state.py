from dataclasses import dataclass, field
from typing import Any, Dict, List


@dataclass
class AgentState:
    """Shared execution state for one unified ANT intelligence run."""

    user_input: str
    user_context: Dict[str, Any] = field(default_factory=dict)
    conversation_id: str | None = None
    execution_plan: List[Dict[str, Any]] = field(default_factory=list)
    selected_capabilities: List[str] = field(default_factory=list)
    current_node: str | None = None
    capability_results: List[Dict[str, Any]] = field(default_factory=list)
    tool_results: List[Dict[str, Any]] = field(default_factory=list)
    memory_context: Dict[str, Any] = field(default_factory=dict)
    verification_results: Dict[str, Any] = field(default_factory=dict)
    final_response: str | None = None
    audit_metadata: Dict[str, Any] = field(default_factory=dict)
    errors: List[str] = field(default_factory=list)

    def record_result(self, capability: str, result: Any, confidence: float = 0.0) -> None:
        self.capability_results.append({
            "capability": capability,
            "result": result,
            "confidence": max(0.0, min(1.0, confidence)),
        })

    def fail(self, message: str) -> None:
        self.errors.append(message)
