"""ANT AI audit logging."""

from ant_common import AuditTrail


class AuditLogger:
    def __init__(self):
        self.trail = AuditTrail()

    @property
    def logs(self):
        return self.trail.entries

    def record(self, event):
        return self.trail.record(event=event)

    def history(self):
        return self.trail.history()
