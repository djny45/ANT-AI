"""ANT AI Swarm Manager
Controls specialized AI agents.
"""

class SwarmManager:
    def __init__(self):
        self.agents = {}

    def add_agent(self, name, agent):
        self.agents[name] = agent

    def dispatch(self, task):
        results = {}
        for name, agent in self.agents.items():
            results[name] = agent.execute(task)
        return results
