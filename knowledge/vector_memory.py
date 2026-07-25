"""ANT AI vector memory foundation."""

class VectorMemory:
    def __init__(self):
        self.entries = []

    def store(self, text, embedding=None):
        self.entries.append({"text": text, "embedding": embedding})

    def search(self, query):
        return self.entries
