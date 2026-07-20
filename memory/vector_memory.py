"""ANT AI vector memory interface."""

class VectorMemory:
    def __init__(self):
        self.memory = []

    def store(self, item):
        self.memory.append(item)

    def retrieve(self, keyword):
        return [x for x in self.memory if keyword.lower() in str(x).lower()]
