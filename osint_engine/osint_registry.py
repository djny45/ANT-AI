"""ANT OSINT resource registry."""

class OSINTRegistry:
    def __init__(self):
        self.resources = []

    def add(self, resource):
        self.resources.append(resource)

    def list_resources(self):
        return self.resources
