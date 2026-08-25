"""
ANT AI Harness execution pipeline.

Connects routing, governance, orchestration, memory and tools into one
controlled execution flow while preserving the unified intelligence core.
"""

from .orchestrator import HarnessOrchestrator
from .router import route_request
from .governance import evaluate_request
from .memory import MemoryStore
from .tools import ToolRegistry


class HarnessPipeline:
    def __init__(self):
        self.orchestrator = HarnessOrchestrator()
        self.memory = MemoryStore()
        self.tools = ToolRegistry()

    def execute(self, request):
        route = route_request(request)

        governance = evaluate_request(request)
        if not governance.get("allowed", True):
            return {"status": "blocked", "reason": governance}

        result = self.orchestrator.execute(
            request=request,
            route=route,
            tools=self.tools,
            memory=self.memory,
        )

        self.memory.store(request, result)

        return {
            "status": "completed",
            "route": route,
            "result": result,
        }
