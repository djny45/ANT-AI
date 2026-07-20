"""ANT AI agent lifecycle manager."""

class AgentManager:
    def __init__(self):
        self.agents = {}

    def add(self, name, agent):
        self.agents[name] = agent

    def list_agents(self):
        return list(self.agents.keys())
