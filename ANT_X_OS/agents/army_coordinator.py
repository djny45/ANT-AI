from ant_common import Registry


class AgentArmyCoordinator:
    def __init__(self):
        self._registry = Registry()

    @property
    def armies(self):
        return self._registry.mapping

    def register_army(self, name, agents):
        self._registry.register(name, agents)

    def dispatch(self, army, task):
        agents = self._registry.get(army) or []
        return {"army": army, "agents": len(agents), "task": task}
