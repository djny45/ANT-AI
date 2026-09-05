"""ANT Runtime memory connector.

Bridge for storing execution knowledge and history.
"""


class MemoryConnector:
    def __init__(self, memory=None):
        self.memory = memory

    def store(self, context, result):
        if self.memory:
            return self.memory.store(context, result)
        return {
            "stored": True,
            "context": context,
            "result": result,
        }

    def recall(self, query):
        if self.memory:
            return self.memory.search(query)
        return []
