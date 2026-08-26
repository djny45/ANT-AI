"""
ANT AI agent runtime adapter.

Provides the integration boundary between the Harness runtime controller
and the ANT AI agent execution implementation.
"""

from typing import Any, Dict, Protocol


class AgentEngine(Protocol):
    def run(self, context: Dict[str, Any]) -> Dict[str, Any]:
        ...


class AgentRuntimeAdapter:
    """Adapts ANT AI agent execution to the runtime interface contract."""

    def __init__(self, engine: AgentEngine):
        self.engine = engine

    def execute(self, context: Dict[str, Any]) -> Dict[str, Any]:
        result = self.engine.run(context)

        return {
            "status": "completed",
            "result": result,
        }
