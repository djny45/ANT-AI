class AgentArmyCoordinator:
    def __init__(self):
        self.armies = {}

    def register_army(self, name, agents):
        self.armies[name] = agents

    def dispatch(self, army, task):
        return {"army": army, "task": task, "status": "assigned"}
