"""ANT Runtime Exception Manager.

Centralized failure classification and recovery hooks.
"""

from dataclasses import dataclass
from datetime import datetime


@dataclass
class RuntimeErrorEvent:
    error_type: str
    message: str
    timestamp: str


class ExceptionManager:
    def __init__(self):
        self.errors = []

    def capture(self, error: Exception):
        event = RuntimeErrorEvent(
            error_type=type(error).__name__,
            message=str(error),
            timestamp=datetime.utcnow().isoformat(),
        )
        self.errors.append(event)
        return event

    def latest(self):
        return self.errors[-1] if self.errors else None
