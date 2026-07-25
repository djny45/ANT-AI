"""ANT AI God Mode agent manager.

Controls registration, capability discovery, and task routing.
"""

class AgentManager:
    def __init__(self):
        self.agents = {}

    def register(self, name, capabilities):
        self.agents[name] = {
            "capabilities": capabilities,
            "status": "ready"
        }

    def find_for_task(self, capability):
        return [
            name for name, agent in self.agents.items()
            if capability in agent["capabilities"]
        ]

    def assign(self, task, capability=None):
        agents = self.find_for_task(capability) if capability else list(self.agents.keys())
        return {
            "task": task,
            "agents": agents,
            "status": "assigned"
        }

    def available_agents(self):
        return self.agents
