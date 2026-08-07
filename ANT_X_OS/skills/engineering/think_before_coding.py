from typing import List, Dict, Any
from ..base_skill import BaseSkill


class ThinkBeforeCoding(BaseSkill):
    def __init__(self):
        super().__init__(
            name="Think Before Coding",
            description="Inspect repo, list assumptions, affected files, and verification steps.",
            rules=[
                "inspect repository first",
                "identify assumptions",
                "list affected files",
                "define verification steps",
            ],
        )

    def validate(self, context: Dict[str, Any]) -> bool:
        # require at least a repo and a brief description
        return bool(context.get("repo") and (context.get("description") or context.get("goal")))

    def execute(self, task: Dict[str, Any], memory=None) -> Dict[str, Any]:
        # create a lightweight plan fragment
        files = task.get("affected_files", [])
        plan = {
            "assumptions": ["runtime available", "tests exist"],
            "files": files,
            "verification": ["unit tests", "lint"]
        }
        return {"skill": self.name, "plan": plan}
