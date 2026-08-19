"""ANT AI God Mode agent manager.

Controls registration, capability discovery, and task routing.
"""

from ant_common import Registry


class AgentManager:
    def __init__(self):
        self._registry = Registry()

    @property
    def agents(self):
        return self._registry.mapping

    def register(self, name, capabilities):
        self._registry.register(name, {
            "capabilities": capabilities,
            "status": "ready"
        })

    def find_for_task(self, capability):
        return [
            name for name, agent in self._registry.mapping.items()
            if capability in agent["capabilities"]
        ]

    def assign(self, task, capability=None):
        agents = self.find_for_task(capability) if capability else self._registry.names()
        return {
            "task": task,
            "agents": agents,
            "status": "assigned"
        }

    def available_agents(self):
        return self._registry.mapping
