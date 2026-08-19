from ant_common import KeywordStore


class VectorMemory:
    def __init__(self):
        self._store = KeywordStore()

    @property
    def items(self):
        return self._store.entries

    def store(self, text, score=1.0):
        return self._store.add(text, score=score)

    def search(self, query):
        return self._store.all()
