"""ANT AI vector memory foundation."""

from ant_common import KeywordStore


class VectorMemory:
    def __init__(self):
        self._store = KeywordStore()

    @property
    def entries(self):
        return self._store.entries

    def store(self, text, embedding=None):
        return self._store.add(text, embedding=embedding)

    def search(self, query):
        return self._store.all()
