"""ANT Runtime Agent Connector

Adapter for routing tasks to the agent system.
"""


class AgentConnector:
    def __init__(self, registry=None):
        self.registry = registry

    def select_agent(self, task):
        if self.registry:
            return self.registry.select(task)
        return {"agent": "default", "task": task}
