from dataclasses import dataclass


@dataclass(frozen=True)
class Decision:
    route: str
    complexity: str
    confidence: float


class DecisionEngine:
    """Selects an execution mode for the single ANT intelligence core."""

    def decide(self, request: str, task_count: int) -> Decision:
        text = request.lower().strip()
        markers = ("build", "implement", "integrate", "architecture", "system", "workflow")

        if task_count > 1 or any(k in text for k in markers):
            return Decision("unified_parallel", "complex", 0.90)
        if task_count == 1 and text:
            return Decision("unified_focused", "focused", 0.82)
        return Decision("unified_direct", "simple", 0.70)
