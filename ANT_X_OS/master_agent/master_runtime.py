"""Master runtime extended to select skills before dispatching to agents and orchestrate them."""
from typing import Any
from ANT_X_OS.master_agent.master_runtime import MasterAgentRuntime as _OldMaster
from ANT_X_OS.skills.loader import load_builtin_skills
from ANT_X_OS.skills.selector import SkillSelector
from ANT_X_OS.skills.orchestrator import SkillOrchestrator


class MasterAgentRuntime(_OldMaster):
    def __init__(self, planner, registry, evaluator=None, memory=None):
        super().__init__(planner, registry, evaluator)
        # ensure skills are available
        load_builtin_skills()
        self.selector = SkillSelector(registry)
        # optional memory instance to persist workflows
        self.memory = memory
        self.orchestrator = SkillOrchestrator(self.selector.registry, memory=self.memory)

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

            # run orchestration (validate/execute skills and record workflow)
            orchestration = self.orchestrator.run(task)
            task["validation"] = orchestration.get("workflow", {})

            agent = self.registry.get(task.get("agent"))
            if agent:
                # dispatch the enriched task to the agent
                results.append(agent.run(task))
            else:
                results.append({"agent": None, "task": task, "status": "no_agent_found", "skills": selected, "validation": orchestration.get("workflow")})

        if self.evaluator:
            return self.evaluator.evaluate(goal, results)
        return results
