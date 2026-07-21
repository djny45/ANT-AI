"""ANT AI agent registry.

Stores available agents for workflow routing.
"""

class AgentRegistry:
    def __init__(self):
        self.agents = {}

    def register(self, name, agent):
        self.agents[name] = agent

    def get(self, name):
        return self.agents.get(name)

    def list_agents(self):
        return list(self.agents.keys())
