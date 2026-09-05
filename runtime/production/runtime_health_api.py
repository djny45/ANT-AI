"""ANT runtime health API foundation."""


class RuntimeHealthAPI:
    def __init__(self, health_monitor=None):
        self.health_monitor = health_monitor

    def check(self):
        if self.health_monitor:
            return self.health_monitor.status()
        return {"healthy": True}
