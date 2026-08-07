from typing import Dict, Any
from .base_skill import BaseSkill


class ReviewSkill(BaseSkill):
    def __init__(self):
        super().__init__(
            name="Review Skill",
            description="Review code for correctness, style, and security.",
            rules=["check logic", "check tests", "check security"],
        )

    def validate(self, context: Dict[str, Any]) -> bool:
        return True

    def execute(self, task: Dict[str, Any], memory=None) -> Dict[str, Any]:
        return {"skill": self.name, "result": "review_passed"}
