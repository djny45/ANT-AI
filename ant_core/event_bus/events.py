from dataclasses import dataclass, field
from typing import Any

from ant_common import utc_timestamp

@dataclass(frozen=True)
class IntelligenceEvent:
    name: str
    payload: dict[str, Any] = field(default_factory=dict)
    timestamp: str = field(default_factory=utc_timestamp)

class EventBus:
    def __init__(self):
        self.events: list[IntelligenceEvent] = []

    def publish(self, name: str, payload: dict[str, Any] | None = None) -> IntelligenceEvent:
        event = IntelligenceEvent(name=name, payload=payload or {})
        self.events.append(event)
        return event
