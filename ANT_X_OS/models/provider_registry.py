class ModelProviderRegistry:
    def __init__(self):
        self.providers = {}

    def register(self, name, client, cost=0, speed=0):
        self.providers[name] = {"client": client, "cost": cost, "speed": speed}

    def best(self, priority="speed"):
        return min(self.providers, key=lambda x: self.providers[x].get(priority, 0), default=None)
