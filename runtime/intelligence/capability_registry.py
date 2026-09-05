"""ANT capability registry.

Tracks available runtime capabilities and providers.
"""


class CapabilityRegistry:
    def __init__(self):
        self.capabilities = {}

    def register(self, name, provider):
        self.capabilities[name] = provider

    def get(self, name):
        return self.capabilities.get(name)

    def list_capabilities(self):
        return list(self.capabilities.keys())
