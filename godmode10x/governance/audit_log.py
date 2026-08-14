"""Godmode 10x Audit Logger."""

from datetime import datetime


class AuditLog:
    def __init__(self):
        self.events = []

    def record(self, event: str, metadata: dict | None = None):
        self.events.append({
            "event": event,
            "metadata": metadata or {},
            "timestamp": datetime.utcnow().isoformat(),
        })

    def history(self):
        return self.events
