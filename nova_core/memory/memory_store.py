"""NOVA Core v0.2 Memory Store prototype.

Provides a minimal experience storage layer for the first runtime.
"""


class MemoryStore:
    def __init__(self):
        self.experiences = []

    def remember(self, experience):
        self.experiences.append(experience)

    def recall(self):
        return list(self.experiences)
