"""ANT AI evolution history storage."""

class EvolutionMemory:
    def __init__(self):
        self.history = []

    def record(self, change):
        self.history.append(change)

    def get_history(self):
        return self.history
