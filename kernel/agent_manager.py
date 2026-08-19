"""ANT AI agent lifecycle manager."""

from ant_common import Registry


class AgentManager:
    def __init__(self):
        self._registry = Registry()

    @property
    def agents(self):
        return self._registry.mapping

    def add(self, name, agent):
        self._registry.register(name, agent)

    def list_agents(self):
        return self._registry.names()
