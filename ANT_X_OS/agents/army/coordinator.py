class AgentArmyCoordinator:
    def __init__(self):
        self.agents = {}

    def register_agent(self, name, agent):
        self.agents[name] = agent

    def assign(self, task):
        for name, agent in self.agents.items():
            return agent.run(task)
        return None
