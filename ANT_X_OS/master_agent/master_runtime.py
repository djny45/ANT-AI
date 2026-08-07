"""Master runtime extended to select skills before dispatching to agents."""
from typing import Any
from ANT_X_OS.master_agent.master_runtime import MasterAgentRuntime as _OldMaster
from ANT_X_OS.skills.loader import load_builtin_skills
from ANT_X_OS.skills.selector import SkillSelector


class MasterAgentRuntime(_OldMaster):
    def __init__(self, planner, registry, evaluator=None):
        super().__init__(planner, registry, evaluator)
        # ensure skills are available
        load_builtin_skills()
        self.selector = SkillSelector(registry)

    def run(self, goal: Any):
        tasks = self.planner.plan(goal)
        results = []
        for task in tasks:
            # attach selected skills for this task
            selected = self.selector.select_for_task(task)
            if isinstance(task, dict):
                task["skills"] = selected
            else:
                task = {"task": task, "skills": selected}

            agent = self.registry.get(task.get("agent"))
            if agent:
                # dispatch the enriched task to the agent
                results.append(agent.run(task))
            else:
                results.append({"agent": None, "task": task, "status": "no_agent_found", "skills": selected})

        if self.evaluator:
            return self.evaluator.evaluate(goal, results)
        return results
