"""ANT AI identity management."""

class IdentityManager:
    def __init__(self):
        self.identities = {}

    def register(self, name, identity):
        self.identities[name] = identity

    def verify(self, name):
        return name in self.identities
