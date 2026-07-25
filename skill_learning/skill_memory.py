"""ANT remembers skill performance."""

class SkillMemory:
    def __init__(self):
        self.history = []

    def record(self, skill, score):
        self.history.append({"skill": skill, "score": score})

    def get_history(self):
        return self.history
