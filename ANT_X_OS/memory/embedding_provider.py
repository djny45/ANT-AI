from ant_common import keyword_filter


class EmbeddingProvider:
    def __init__(self, backend="local"):
        self.backend = backend

    def embed(self, text):
        return [float(len(text))]


class VectorMemoryBackend:
    def __init__(self, store=None):
        self.store = store or []

    def add(self, text):
        self.store.append(text)

    def search(self, query):
        return keyword_filter(self.store, query)
