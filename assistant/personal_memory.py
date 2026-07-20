"""ANT AI personal memory foundation."""

class PersonalMemory:
    def __init__(self):
        self.memories = []

    def remember(self, item):
        self.memories.append(item)

    def recall(self):
        return self.memories
