class ModelRouter:
    def __init__(self):
        self.providers = {}

    def register(self, name, provider, capability):
        self.providers[name] = {"provider": provider, "capability": capability}

    def select(self, requirement):
        for name, data in self.providers.items():
            if requirement in data["capability"]:
                return name
        return None
