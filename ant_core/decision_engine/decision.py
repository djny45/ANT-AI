from dataclasses import dataclass

@dataclass(frozen=True)
class Decision:
    route: str
    complexity: str
    confidence: float

class DecisionEngine:
    def decide(self, request: str, task_count: int) -> Decision:
        text = request.lower()
        markers = ("build", "implement", "integrate", "architecture", "system", "workflow")
        if task_count > 1 or any(k in text for k in markers):
            return Decision("multi_agent", "complex", 0.90)
        if task_count == 1 and text.strip():
            return Decision("specialist", "focused", 0.82)
        return Decision("direct", "simple", 0.70)
