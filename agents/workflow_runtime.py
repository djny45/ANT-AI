"""ANT AI workflow execution runtime."""


class WorkflowRuntime:
    def __init__(self, agents=None, state=None):
        self.agents = agents or {}
        self.state = state

    async def execute(self, workflow):
        results = []
        for step in workflow.get("steps", []):
            agent = self.agents.get(step.get("agent"))
            if not agent:
                result = {"error": "agent unavailable", "step": step}
            else:
                try:
                    result = await agent.execute(step)
                except Exception as exc:
                    result = {"error": str(exc), "step": step}
            results.append(result)
            if self.state:
                self.state.log_execution(step, result)
        return {"goal": workflow.get("goal"), "results": results, "status": "completed"}
