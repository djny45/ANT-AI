"""ANT AI version management."""

class VersionManager:
    def __init__(self):
        self.versions = []

    def record(self, version):
        self.versions.append(version)

    def history(self):
        return self.versions
