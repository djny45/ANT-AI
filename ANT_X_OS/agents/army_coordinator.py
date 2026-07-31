class AgentArmyCoordinator:
    def __init__(self):
        self.armies = {}

    def register_army(self, name, agents):
        self.armies[name] = agents

    def dispatch(self, army, task):
        agents = self.armies.get(army, [])
        return {"army": army, "agents": len(agents), "task": task}
