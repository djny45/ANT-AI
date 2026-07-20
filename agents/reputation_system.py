"""ANT agent performance reputation."""

class ReputationSystem:
    def __init__(self):
        self.scores = {}

    def update(self, agent, score):
        self.scores[agent] = score

    def get(self, agent):
        return self.scores.get(agent, 0)
