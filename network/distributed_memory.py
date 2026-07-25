"""ANT AI distributed memory sharing."""

class DistributedMemory:
    def __init__(self):
        self.nodes = []

    def share(self, memory):
        self.nodes.append(memory)

    def get_all(self):
        return self.nodes
