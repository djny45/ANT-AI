class VectorMemory:
    def __init__(self):
        self.items = []

    def store(self, text, metadata=None):
        self.items.append({"text": text, "metadata": metadata or {}})

    def search(self, query):
        return [x for x in self.items if query.lower() in x["text"].lower()]
