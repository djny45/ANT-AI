"""ANT production monitoring foundation."""


class Monitoring:
    def __init__(self):
        self.events = []

    def record(self, event):
        self.events.append(event)

    def status(self):
        return {"events": len(self.events), "healthy": True}
