"""ANT AI Harness execution service.

Connects the API layer with the internal harness pipeline
and tracks execution lifecycle states.
"""

from .pipeline import HarnessPipeline
from .execution_status import ExecutionStatus
from .execution_history import ExecutionHistory


class HarnessExecutionService:
    def __init__(self):
        self.pipeline = HarnessPipeline()
        self.status = ExecutionStatus()
        self.history = ExecutionHistory()

    def execute(self, request):
        execution_id = self.status.start(request)
        self.history.record_start(execution_id, request)

        try:
            result = self.pipeline.execute(request)
            self.status.complete(execution_id, result)
            self.history.record_complete(execution_id, result)
            return {
                "execution_id": execution_id,
                "status": "completed",
                "result": result,
            }
        except Exception as error:
            self.status.fail(execution_id, str(error))
            self.history.record_failure(execution_id, str(error))
            return {
                "execution_id": execution_id,
                "status": "failed",
                "error": str(error),
            }
