from dataclasses import dataclass
from typing import List, Dict, Any

@dataclass
class Skill:
    name: str
    description: str
    rules: List[str]

    def validate(self, context: Dict[str, Any]) -> bool:
        """Basic validation to be overridden by concrete skills.

        Returns True when context satisfies the skill's validation rules.
        """
        # Default: minimal validation — ensure a `repo` key is present
        return "repo" in context


class BaseSkill(Skill):
    def __init__(self, name: str, description: str, rules: List[str]):
        super().__init__(name, description, rules)

    def execute(self, task: Dict[str, Any], memory=None) -> Dict[str, Any]:
        """Execute the skill logic. Concrete skills should override."""
        return {"skill": self.name, "result": "noop"}
