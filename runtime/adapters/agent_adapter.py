"""Agent adapter for ANT Runtime integration."""

class AgentAdapter:
    def __init__(self, registry=None):
        self.registry = registry

    def select_agent(self, task):
        if self.registry and hasattr(self.registry, "select"):
            return self.registry.select(task)
        return {"agent": "default", "task": task}
