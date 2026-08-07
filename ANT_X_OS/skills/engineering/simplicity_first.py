from typing import Dict, Any
from ..base_skill import BaseSkill


class SimplicityFirst(BaseSkill):
    def __init__(self):
        super().__init__(
            name="Simplicity First",
            description="Prefer the simplest implementation that satisfies the spec.",
            rules=["small changes", "avoid premature optimization", "prefer clarity"]
        )

    def validate(self, context: Dict[str, Any]) -> bool:
        return True

    def execute(self, task: Dict[str, Any], memory=None) -> Dict[str, Any]:
        return {"skill": self.name, "result": "favor_simple_solution"}
