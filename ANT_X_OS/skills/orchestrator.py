from typing import Any

from .registry import registry as default_registry


class SkillOrchestrator:
    """Orchestrates validation and execution of a list of skills for a task.

    - Validates each skill against a lightweight context
    - Executes skill.execute(task, memory) when validation passes
    - Records validation_results and stores a workflow snapshot into memory when available
    """

    def __init__(self, registry=None, memory=None):
        self.registry = registry or default_registry
        self.memory = memory

    def run(self, task: dict[str, Any]) -> dict[str, Any]:
        skills: list[str] = task.get("skills", [])
        context = {
            "repo": task.get("repo"),
            "description": task.get("description"),
            "goal": task.get("goal"),
        }

        validation_results: dict[str, dict[str, Any]] = {}
        overall = True

        for name in skills:
            skill = self.registry.get(name)
            if not skill:
                validation_results[name] = {"validated": False, "reason": "not_registered"}
                overall = False
                continue

            try:
                valid = bool(skill.validate(context))
            except Exception as e:  # noqa: BLE001
                validation_results[name] = {"validated": False, "reason": f"validate_error: {e}"}
                overall = False
                continue

            if not valid:
                validation_results[name] = {"validated": False, "reason": "validation_failed"}
                overall = False
                continue

            # run the skill
            try:
                result = skill.execute(task, memory=self.memory)
                validation_results[name] = {"validated": True, "result": result}
            except Exception as e:  # noqa: BLE001
                validation_results[name] = {"validated": False, "reason": f"execute_error: {e}"}
                overall = False

        workflow = {"task": task.get("task") or task, "skills": skills, "validation": validation_results, "success": overall}

        if self.memory:
            try:
                self.memory.store_workflow(workflow)
            except Exception:  # noqa: BLE001, S110
                # be resilient to memory errors
                pass

        return {"workflow": workflow}
