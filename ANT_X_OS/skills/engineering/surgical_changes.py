from typing import Dict, Any
from ..base_skill import BaseSkill


class SurgicalChanges(BaseSkill):
    def __init__(self):
        super().__init__(
            name="Surgical Changes",
            description="Make minimal, well-scoped changes with clear diffs.",
            rules=["small commits", "targeted files", "update tests"]
        )

    def validate(self, context: Dict[str, Any]) -> bool:
        return True

    def execute(self, task: Dict[str, Any], memory=None) -> Dict[str, Any]:
        return {"skill": self.name, "result": "surgical_patch_plan"}
