"""ANT AI Harness execution service.

Connects the API layer with the internal harness pipeline.
"""

from .pipeline import HarnessPipeline


class HarnessExecutionService:
    def __init__(self):
        self.pipeline = HarnessPipeline()

    def execute(self, request):
        return self.pipeline.run(request)
