"""ANT AI goal engine with persistence and planning."""

import json


class GoalEngine:
    def __init__(self, state, llm):
        self.state = state
        self.llm = llm

    async def create_goal(self, objective):
        prompt = (
            "Break this goal into 2 or 3 concrete executable subtasks. "
            "Return JSON list only. Goal: " + objective
        )
        response = await self.llm.generate(prompt)
        try:
            subtasks = json.loads(response)
        except Exception:
            subtasks = [{"task": objective}]

        goal_id = self.state.save_goal(objective, subtasks)
        return {
            "id": goal_id,
            "goal": objective,
            "subtasks": subtasks,
            "status": "created"
        }
