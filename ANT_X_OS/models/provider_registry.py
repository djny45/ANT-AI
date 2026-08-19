from ant_common import Registry


class ModelProviderRegistry:
    def __init__(self):
        self._registry = Registry()

    @property
    def providers(self):
        return self._registry.mapping

    def register(self, name, client, cost=0, speed=0):
        self._registry.register(name, {"client": client, "cost": cost, "speed": speed})

    def best(self, priority="speed"):
        providers = self._registry.mapping
        return min(providers, key=lambda x: providers[x].get(priority, 0), default=None)
