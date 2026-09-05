"""Adaptive memory management foundation for ANT learning."""

class AdaptiveMemoryManager:
    def __init__(self):
        self.memory = []

    def store(self, experience):
        self.memory.append(experience)

    def retrieve(self, limit=5):
        return self.memory[-limit:]
