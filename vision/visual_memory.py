"""ANT AI visual memory storage."""

class VisualMemory:
    def __init__(self):
        self.items = []

    def store(self, visual_data):
        self.items.append(visual_data)

    def recall(self):
        return self.items
