"""Skill selector maps tasks to required skills."""
from typing import List, Dict, Any
from .registry import registry


class SkillSelector:
    def __init__(self, registry=None):
        self.registry = registry or registry

    def select_for_task(self, task: Dict[str, Any]) -> List[str]:
        """Return a list of skill names based on simple heuristics in task dict.

        Task can be a string or a dict with `type` or `description`.
        """
        text = ""
        if isinstance(task, dict):
            text = (task.get("type", "") + " " + task.get("description", "")).lower()
        else:
            text = str(task).lower()

        skills = set()
        if "code" in text or "implement" in text or "feature" in text:
            skills.update(["Coding Skill", "Review Skill", "Security Skill"])
        if "bug" in text or "fix" in text or "error" in text:
            skills.update(["Debugging Skill", "Review Skill"])
        if "deploy" in text or "release" in text or "rollback" in text:
            skills.update(["Deployment Skill", "Security Skill"])
        if "design" in text or "architecture" in text or "plan" in text:
            skills.update(["Think Before Coding", "Goal Driven Execution"])

        # fallback: add a thinking heuristic
        if not skills:
            skills.add("Think Before Coding")

        # return only those skills that exist in the registry
        return [name for name in skills if self.registry.get(name)]
