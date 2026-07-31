class VectorMemoryEngine:
    def __init__(self):
        self.records = []

    def add(self, content, metadata=None):
        self.records.append({"content": content, "metadata": metadata or {}})

    def retrieve(self, query):
        return [r for r in self.records if query.lower() in r["content"].lower()]
