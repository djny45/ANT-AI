from typing import Any

from .base_skill import BaseSkill


class ResearchSkill(BaseSkill):
    def __init__(self):
        super().__init__(
            name="Research Skill",
            description="Investigate questions and structure relevant findings.",
            rules=["gather evidence", "compare sources", "summarize findings"],
        )

    def validate(self, context: dict[str, Any]) -> bool:
        return True

    def execute(self, task: dict[str, Any], memory=None) -> dict[str, Any]:
        return {"skill": self.name, "result": "research_plan_ready"}
