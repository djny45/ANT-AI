"""ANT AI Harness execution service.

Connects the API layer with the internal harness pipeline
and tracks execution lifecycle states.
"""

from .pipeline import HarnessPipeline
from .execution_status import ExecutionStatus


class HarnessExecutionService:
    def __init__(self):
        self.pipeline = HarnessPipeline()
        self.status = ExecutionStatus()

    def execute(self, request):
        execution_id = self.status.start(request)

        try:
            result = self.pipeline.run(request)
            self.status.complete(execution_id, result)
            return {
                "execution_id": execution_id,
                "status": "completed",
                "result": result,
            }
        except Exception as error:
            self.status.fail(execution_id, str(error))
            return {
                "execution_id": execution_id,
                "status": "failed",
                "error": str(error),
            }
