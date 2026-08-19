"""ANT AI vector memory interface."""

from ant_common import keyword_filter


class VectorMemory:
    def __init__(self):
        self.memory = []

    def store(self, item):
        self.memory.append(item)

    def retrieve(self, keyword):
        return keyword_filter(self.memory, keyword)
