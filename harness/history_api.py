"""ANT AI Harness execution history query layer.

Provides read access to execution audit records.
"""

from .execution_history import ExecutionHistory


class ExecutionHistoryAPI:
    def __init__(self):
        self.history = ExecutionHistory()

    def list_executions(self):
        return self.history.records()

    def get_execution(self, execution_id):
        return self.history.get(execution_id)
