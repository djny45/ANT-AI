"""
ANT AI LangGraph Master Planner Bridge

Connects graph execution with the existing Master Agent layer.
"""

from typing import Any, Dict


class MasterPlannerBridge:
    """Adapter between graph state and ANT AI Master Agent."""

    def __init__(self, master_agent=None):
        self.master_agent = master_agent

    async def create_plan(self, state: Dict[str, Any]) -> Dict[str, Any]:
        user_input = state.get("user_input", "")

        if self.master_agent:
            result = await self.master_agent.receive_request(user_input)
            return {
                "execution_plan": result,
                "planner": "master_agent"
            }

        return {
            "execution_plan": {
                "goal": user_input,
                "tasks": [],
                "agents": []
            },
            "planner": "fallback"
        }

    async def route_plan(self, plan: Dict[str, Any]):
        tasks = plan.get("tasks", [])
        return {
            "selected_agents": [task.get("agent") for task in tasks]
        }
