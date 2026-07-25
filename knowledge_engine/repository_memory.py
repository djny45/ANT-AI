"""ANT AI repository memory storage."""

class RepositoryMemory:
    def __init__(self):
        self.repositories = []

    def store(self, repository):
        self.repositories.append(repository)

    def list(self):
        return self.repositories
