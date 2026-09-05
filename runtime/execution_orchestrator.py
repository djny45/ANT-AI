"""ANT unified execution orchestrator.

Coordinates goal processing, agent execution,
workflow execution, verification and memory hooks.
"""


class ExecutionOrchestrator:
    def __init__(self, goal_bridge=None, agent_bridge=None, workflow_bridge=None):
        self.goal_bridge = goal_bridge
        self.agent_bridge = agent_bridge
        self.workflow_bridge = workflow_bridge

    def execute(self, goal):
        plan = self._plan(goal)
        agent_result = self._run_agent(plan)
        workflow_result = self._run_workflow(agent_result)

        return {
            "goal": goal,
            "plan": plan,
            "result": workflow_result,
            "status": "completed"
        }

    def _plan(self, goal):
        if self.goal_bridge:
            return self.goal_bridge.execute(goal)
        return {"goal": goal}

    def _run_agent(self, plan):
        if self.agent_bridge:
            return self.agent_bridge.execute(plan)
        return plan

    def _run_workflow(self, result):
        if self.workflow_bridge:
            return self.workflow_bridge.execute(result)
        return result
