"""ANT AI resource management."""

class ResourceManager:
    def __init__(self):
        self.resources = {}

    def register(self, name, value):
        self.resources[name] = value

    def status(self):
        return self.resources
