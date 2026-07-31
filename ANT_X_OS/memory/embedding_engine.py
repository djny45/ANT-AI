class EmbeddingEngine:
    def embed(self, text):
        return [ord(c) for c in text[:32]]


class VectorMemoryV2:
    def __init__(self):
        self.records = []
        self.engine = EmbeddingEngine()

    def add(self, text, metadata=None):
        self.records.append({
            "text": text,
            "vector": self.engine.embed(text),
            "metadata": metadata or {}
        })

    def all(self):
        return self.records
