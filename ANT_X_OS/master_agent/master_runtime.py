"""Master runtime for planning, skill selection and agent dispatch."""
from typing import Any

from ANT_X_OS.skills.loader import load_builtin_skills
from ANT_X_OS.skills.orchestrator import SkillOrchestrator
from ANT_X_OS.skills.selector import SkillSelector


class MasterAgentRuntime:
    def __init__(self, planner, registry, evaluator=None, memory=None):
        self.planner = planner
        self.registry = registry
        self.evaluator = evaluator
        load_builtin_skills()
        self.selector = SkillSelector()
        self.memory = memory
        self.orchestrator = SkillOrchestrator(self.selector.registry, memory=self.memory)

    def run(self, goal: Any):
        tasks = self.planner.plan(goal)
        if isinstance(tasks, dict):
            tasks = tasks.get("tasks", [tasks])
        results = []
        for task in tasks:
            task = dict(task) if isinstance(task, dict) else {"task": task}
            selected = self.selector.select_for_task(task)
            task["skills"] = selected

            orchestration = self.orchestrator.run(task)
            task["validation"] = orchestration.get("workflow", {})

            agent_name = task.get("agent")
            if hasattr(self.registry, "get"):
                agent = self.registry.get(agent_name)
            else:
                agent = None
            if agent:
                results.append(agent.run(task))
            else:
                results.append({
                    "agent": agent_name,
                    "task": task,
                    "status": "no_agent_found",
                    "skills": selected,
                    "validation": orchestration.get("workflow"),
                })

        if self.evaluator:
            try:
                return self.evaluator.evaluate(results)
            except TypeError:
                return self.evaluator.evaluate(goal, results)
        return results
