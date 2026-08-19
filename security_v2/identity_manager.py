"""ANT AI identity management."""

from ant_common import Registry


class IdentityManager:
    def __init__(self):
        self._registry = Registry()

    @property
    def identities(self):
        return self._registry.mapping

    def register(self, name, identity):
        self._registry.register(name, identity)

    def verify(self, name):
        return name in self._registry
