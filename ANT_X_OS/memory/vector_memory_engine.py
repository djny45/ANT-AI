from ant_common import KeywordStore


class VectorMemoryEngine:
    def __init__(self):
        self._store = KeywordStore("content")

    @property
    def records(self):
        return self._store.entries

    def add(self, content, metadata=None):
        return self._store.add(content, metadata=metadata or {})

    def retrieve(self, query):
        return self._store.search(query)
