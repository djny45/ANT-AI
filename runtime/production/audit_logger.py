"""ANT execution audit logging foundation."""


class AuditLogger:
    def __init__(self):
        self.logs = []

    def log(self, action, details=None):
        self.logs.append({"action": action, "details": details})

    def history(self):
        return self.logs
