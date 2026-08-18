"""ANT AI graph pipeline integration.

Connects graph orchestration with existing ANT-X-OS runtime components.
"""

from typing import Any, Dict


class ANTAIGraphPipeline:
    """Execution bridge for User -> Graph -> Agents -> Response."""

    def __init__(self, graph, bridge, audit=None, memory=None):
        self.graph = graph
        self.bridge = bridge
        self.audit = audit
        self.memory = memory

    async def execute(self, user_input: str, context: Dict[str, Any] | None = None):
        state = {
            "user_input": user_input,
            "context": context or {},
            "results": [],
            "agent_results": [],
            "final_response": None,
        }

        if self.audit:
            self.audit.log({"event": "graph_execution_started", "input": user_input})

        result = await self.graph.run(state) if hasattr(self.graph, "run") else self.graph.execute(state)

        if self.memory and result.get("final_response"):
            self.memory.save(result["final_response"])

        if self.audit:
            self.audit.log({"event": "graph_execution_completed"})

        return result
