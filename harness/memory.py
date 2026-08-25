"""ANT AI Harness memory boundary.

Initial abstraction for future persistent memory systems.
"""


class Memory:
    def __init__(self):
        self.context = []

    def store(self, item):
        self.context.append(item)

    def retrieve(self):
        return self.context
