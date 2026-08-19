from dataclasses import dataclass, field
from typing import Any


@dataclass
class IntelligenceState:
    """Execution state owned by the central intelligence layer."""
    request: str
    context: dict[str, Any] = field(default_factory=dict)
    plan: list[dict[str, Any]] = field(default_factory=list)
    selected_agents: list[str] = field(default_factory=list)
    strategy: str = "PENDING"
    required_capabilities: list[str] = field(default_factory=list)
    confidence: float = 0.0
    intent: str = "PENDING"
    complexity: str = "PENDING"
    results: list[dict[str, Any]] = field(default_factory=list)
    risk_score: float = 0.0
    decision: str = "PENDING"
    status: str = "created"
    errors: list[str] = field(default_factory=list)

    def add_result(self, agent: str, result: Any, confidence: float = 0.0) -> None:
        self.results.append({"agent": agent, "result": result, "confidence": max(0.0, min(1.0, confidence))})
