"""ANT AI audit logging."""

class AuditLogger:
    def __init__(self):
        self.logs = []

    def record(self, event):
        self.logs.append(event)

    def history(self):
        return self.logs
