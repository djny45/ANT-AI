"""ANT unified execution orchestrator.

Coordinates goal processing, intelligence decisions, agent execution,
workflow execution, verification and resilience hooks.
"""


class ExecutionOrchestrator:
    def __init__(self, goal_bridge=None, agent_bridge=None, workflow_bridge=None,
                 recovery_manager=None, metrics=None, intelligence_bridge=None):
        self.goal_bridge = goal_bridge
        self.agent_bridge = agent_bridge
        self.workflow_bridge = workflow_bridge
        self.recovery_manager = recovery_manager
        self.metrics = metrics
        self.intelligence_bridge = intelligence_bridge

    def execute(self, goal):
        try:
            if self.metrics:
                self.metrics.start_execution()

            context = self._prepare_intelligence(goal)
            plan = self._plan(goal, context)
            agent_result = self._run_agent(plan)
            workflow_result = self._run_workflow(agent_result)

            result = {
                "goal": goal,
                "context": context,
                "plan": plan,
                "result": workflow_result,
                "status": "completed"
            }

            if self.metrics:
                self.metrics.record_success()

            return result

        except Exception as error:
            if self.metrics:
                self.metrics.record_failure(error)

            if self.recovery_manager:
                return self.recovery_manager.recover(error, goal)

            raise

    def _prepare_intelligence(self, goal):
        if self.intelligence_bridge:
            return self.intelligence_bridge.analyze(goal)
        return {}

    def _plan(self, goal, context=None):
        if self.goal_bridge:
            return self.goal_bridge.execute({"goal": goal, "context": context})
        return {"goal": goal, "context": context}

    def _run_agent(self, plan):
        if self.agent_bridge:
            return self.agent_bridge.execute(plan)
        return plan

    def _run_workflow(self, result):
        if self.workflow_bridge:
            return self.workflow_bridge.execute(result)
        return result
