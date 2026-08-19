from ant_common import Registry


class ModelRouter:
    def __init__(self):
        self._registry = Registry()

    @property
    def providers(self):
        return self._registry.mapping

    def register(self, name, provider, capability):
        self._registry.register(name, {"provider": provider, "capability": capability})

    def select(self, requirement):
        for name, data in self._registry.mapping.items():
            if requirement in data["capability"]:
                return name
        return None
