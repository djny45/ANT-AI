"""Minimal NOVA nano-capability agent prototype."""


class NanoAgent:
    def __init__(self, name, capability):
        self.name = name
        self.capability = capability
        self.active = True

    def execute(self, task):
        return {
            "agent": self.name,
            "capability": self.capability,
            "task": task,
            "status": "completed",
        }
