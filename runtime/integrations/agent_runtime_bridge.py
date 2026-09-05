"""Bridge between ANT runtime and agent subsystem."""


class AgentRuntimeBridge:
    def __init__(self, registry=None):
        self.registry = registry

    def assign(self, task):
        if self.registry and hasattr(self.registry, "assign"):
            return self.registry.assign(task)
        return {"status": "pending", "task": task}
