"""
ANT AI Graph Runtime - Agent Manager Bridge

Connects graph execution with existing ANT AI agent routing.
The bridge keeps existing agents intact and provides a graph-friendly interface.
"""

from dataclasses import dataclass, field
from typing import Any, Dict, List


@dataclass
class AgentExecutionRequest:
    task: str
    context: Dict[str, Any] = field(default_factory=dict)
    selected_agents: List[str] = field(default_factory=list)


class AgentManagerBridge:
    """Adapter between graph nodes and ANT AI agent manager."""

    def __init__(self, agent_manager=None):
        self.agent_manager = agent_manager

    async def route(self, request: AgentExecutionRequest) -> Dict[str, Any]:
        if self.agent_manager:
            return await self.agent_manager.execute(
                task=request.task,
                agents=request.selected_agents,
                context=request.context,
            )

        return {
            "status": "ready",
            "agents": request.selected_agents,
            "message": "Agent manager bridge initialized"
        }
