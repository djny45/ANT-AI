from typing import Dict, Any
from .base_skill import BaseSkill


class DebuggingSkill(BaseSkill):
    def __init__(self):
        super().__init__(
            name="Debugging Skill",
            description="Identify root causes, reproduce locally, and propose fixes.",
            rules=["reproduce", "isolate", "fix_and_test"],
        )

    def validate(self, context: Dict[str, Any]) -> bool:
        return True

    def execute(self, task: Dict[str, Any], memory=None) -> Dict[str, Any]:
        return {"skill": self.name, "result": "diagnosis_suggested"}
