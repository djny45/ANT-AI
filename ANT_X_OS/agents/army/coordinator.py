from ant_common import Registry


class AgentArmyCoordinator:
    def __init__(self):
        self._registry = Registry()

    @property
    def agents(self):
        return self._registry.mapping

    def register_agent(self, name, agent):
        self._registry.register(name, agent)

    def assign(self, task):
        for agent in self._registry.values():
            return agent.run(task)
        return None
