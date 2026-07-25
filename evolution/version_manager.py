"""ANT AI version tracking."""

class VersionManager:
    def __init__(self):
        self.version = "0.5"

    def current(self):
        return self.version

    def upgrade(self, version):
        self.version = version
        return self.version
