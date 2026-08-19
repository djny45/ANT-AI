"""ANT AI connector manager."""

from ant_common import Registry


class ConnectorManager:
    def __init__(self):
        self._registry = Registry()

    @property
    def connectors(self):
        return self._registry.mapping

    def register(self, name, connector):
        self._registry.register(name, connector)

    def list_connectors(self):
        return self._registry.names()

    def get(self, name):
        return self._registry.get(name)
