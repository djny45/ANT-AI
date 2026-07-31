class VectorMemory:
    def __init__(self):
        self.items = []

    def store(self, text, score=1.0):
        self.items.append({"text": text, "score": score})

    def search(self, query):
        return self.items
