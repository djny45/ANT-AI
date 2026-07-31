class ModelProvider:
    def __init__(self, name, capability):
        self.name = name
        self.capability = capability

    def run(self, prompt):
        return {"provider": self.name, "response": prompt}


class ProviderRegistry:
    def __init__(self):
        self.providers = {}

    def add(self, provider):
        self.providers[provider.name] = provider
