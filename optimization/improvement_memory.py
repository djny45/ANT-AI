"""Stores optimization feedback for future ANT runtime improvements."""

class ImprovementMemory:
    def __init__(self):
        self.records = []

    def add(self, record):
        self.records.append(record)

    def history(self):
        return self.records
