"""ANT AI connector manager."""

class ConnectorManager:
    def __init__(self):
        self.connectors = {}

    def register(self, name, connector):
        self.connectors[name] = connector

    def list_connectors(self):
        return list(self.connectors.keys())

    def get(self, name):
        return self.connectors.get(name)
