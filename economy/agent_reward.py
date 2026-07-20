"""ANT AI agent performance rewards."""

class AgentReward:
    def __init__(self):
        self.scores = {}

    def reward(self, agent, value):
        self.scores[agent] = self.scores.get(agent, 0) + value

    def score(self, agent):
        return self.scores.get(agent, 0)
