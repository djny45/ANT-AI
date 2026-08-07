from typing import Dict, Any
from ..base_skill import BaseSkill


class GoalDrivenExecution(BaseSkill):
    def __init__(self):
        super().__init__(
            name="Goal Driven Execution",
            description="Drive work towards measurable goals and verification criteria.",
            rules=["define goals", "measure against goals", "iterate"]
        )

    def validate(self, context: Dict[str, Any]) -> bool:
        return bool(context.get("goal"))

    def execute(self, task: Dict[str, Any], memory=None) -> Dict[str, Any]:
        return {"skill": self.name, "result": {"goal": task.get("goal")}}
