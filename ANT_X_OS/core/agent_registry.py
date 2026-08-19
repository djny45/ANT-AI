from ant_common import Registry


class AgentRegistry:
    def __init__(self):
        self._registry = Registry()

    @property
    def agents(self):
        return self._registry.mapping

    def register(self, name, agent):
        self._registry.register(name, agent)

    def get(self, name):
        return self._registry.get(name)
