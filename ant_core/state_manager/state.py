from dataclasses import dataclass, field
from typing import Any


@dataclass
class IntelligenceState:
    """Execution state owned by the single ANT intelligence core."""

    request: str
    context: dict[str, Any] = field(default_factory=dict)
    plan: list[dict[str, Any]] = field(default_factory=list)
    selected_capabilities: list[str] = field(default_factory=list)
    results: list[dict[str, Any]] = field(default_factory=list)
    risk_score: float = 0.0
    decision: str = "PENDING"
    status: str = "created"
    errors: list[str] = field(default_factory=list)

    def add_result(self, capability: str, result: Any, confidence: float = 0.0) -> None:
        """Record a result produced by a temporary internal capability."""
        self.results.append(
            {
                "capability": capability,
                "result": result,
                "confidence": max(0.0, min(1.0, confidence)),
            }
        )
