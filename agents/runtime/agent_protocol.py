from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any

@dataclass(frozen=True)
class AgentMessage:
    sender: str
    receiver: str
    objective: str
    context: dict[str, Any] = field(default_factory=dict)
    priority: str = "normal"
    confidence: float = 0.0
    result: Any = None
    timestamp: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())

    def validate(self) -> None:
        if not self.sender or not self.receiver or not self.objective:
            raise ValueError("sender, receiver and objective are required")
        if not 0.0 <= self.confidence <= 1.0:
            raise ValueError("confidence must be between 0 and 1")
