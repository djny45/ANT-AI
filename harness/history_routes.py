"""ANT AI Harness execution history routes.

Provides API route handlers for execution audit retrieval.
"""

from .history_api import ExecutionHistoryAPI


class HistoryRoutes:
    def __init__(self):
        self.history_api = ExecutionHistoryAPI()

    def list_executions(self):
        return self.history_api.get_history()
