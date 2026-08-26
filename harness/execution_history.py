"""
ANT AI Harness execution history storage layer.

Tracks completed execution lifecycle records for future persistence.
"""


class ExecutionHistory:
    def __init__(self):
        self.records = []

    def add(self, execution_record):
        self.records.append(execution_record)
        return execution_record

    def list_all(self):
        return self.records
