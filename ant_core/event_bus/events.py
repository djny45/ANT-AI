from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any

@dataclass(frozen=True)
class IntelligenceEvent:
    name: str
    payload: dict[str, Any] = field(default_factory=dict)
    timestamp: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())

class EventBus:
    def __init__(self):
        self.events: list[IntelligenceEvent] = []

    def publish(self, name: str, payload: dict[str, Any] | None = None) -> IntelligenceEvent:
        event = IntelligenceEvent(name=name, payload=payload or {})
        self.events.append(event)
        return event
