"""ANT execution memory foundation."""


class ExecutionMemory:
    def __init__(self):
        self.records = []

    def store(self, record):
        self.records.append(record)

    def recall(self):
        return self.records
