"""ANT AI goal engine with persistence and planning."""

import json
import logging

logger = logging.getLogger(__name__)


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
        parse_error = None
        try:
            subtasks = json.loads(response)
        except (json.JSONDecodeError, TypeError) as error:
            logger.warning(
                "Planner returned unparsable subtask JSON, falling back to single subtask (%s: %s)",
                type(error).__name__,
                error,
            )
            parse_error = {"error_type": type(error).__name__, "error": str(error)}
            subtasks = [{"task": objective}]

        goal_id = self.state.save_goal(objective, subtasks)
        result = {
            "id": goal_id,
            "goal": objective,
            "subtasks": subtasks,
            "status": "created",
            "subtask_source": "fallback" if parse_error else "planner"
        }
        if parse_error:
            result["planner_error"] = parse_error
        return result
