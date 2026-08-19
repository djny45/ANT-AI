from ant_common import KeywordStore


class VectorMemory:
    def __init__(self):
        self._store = KeywordStore()

    @property
    def items(self):
        return self._store.entries

    def store(self, text, metadata=None):
        return self._store.add(text, metadata=metadata or {})

    def search(self, query):
        return self._store.search(query)
