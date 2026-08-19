"""Godmode 10x Audit Logger."""

from ant_common import AuditTrail


class AuditLog:
    def __init__(self):
        self.trail = AuditTrail()

    @property
    def events(self):
        return self.trail.entries

    def record(self, event: str, metadata: dict | None = None):
        return self.trail.record(event=event, metadata=metadata or {})

    def history(self):
        return self.trail.history()
