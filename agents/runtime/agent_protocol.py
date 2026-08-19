from dataclasses import dataclass, field
from typing import Any

from ant_common import utc_timestamp

@dataclass(frozen=True)
class AgentMessage:
    sender: str
    receiver: str
    objective: str
    context: dict[str, Any] = field(default_factory=dict)
    priority: str = "normal"
    confidence: float = 0.0
    result: Any = None
    timestamp: str = field(default_factory=utc_timestamp)

    def validate(self) -> None:
        if not self.sender or not self.receiver or not self.objective:
            raise ValueError("sender, receiver and objective are required")
        if not 0.0 <= self.confidence <= 1.0:
            raise ValueError("confidence must be between 0 and 1")
