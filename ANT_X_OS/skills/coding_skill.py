from typing import Dict, Any
from .base_skill import BaseSkill


class CodingSkill(BaseSkill):
    def __init__(self):
        super().__init__(
            name="Coding Skill",
            description="Write implementation code following project conventions.",
            rules=["run tests", "respect style", "small commits"],
        )

    def validate(self, context: Dict[str, Any]) -> bool:
        # ensure repo info and files to change
        return bool(context.get("repo"))

    def execute(self, task: Dict[str, Any], memory=None) -> Dict[str, Any]:
        return {"skill": self.name, "result": "code_changes_predicted"}
