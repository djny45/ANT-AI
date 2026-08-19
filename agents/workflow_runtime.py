"""ANT AI workflow execution runtime."""

import logging

logger = logging.getLogger(__name__)


class WorkflowRuntime:
    def __init__(self, agents=None, state=None):
        self.agents = agents or {}
        self.state = state

    async def execute(self, workflow):
        results = []
        errors = []
        for step in workflow.get("steps", []):
            agent_name = step.get("agent")
            agent = self.agents.get(agent_name)
            if not agent:
                logger.error("Workflow step requested unavailable agent: %s", agent_name)
                result = {"error": "agent unavailable", "error_type": "AgentUnavailable", "step": step}
                errors.append(result)
            else:
                try:
                    result = await agent.execute(step)
                except Exception as exc:
                    logger.exception("Workflow step failed on agent %s", agent_name)
                    result = {"error": str(exc), "error_type": type(exc).__name__, "step": step}
                    errors.append(result)
            results.append(result)
            if self.state:
                try:
                    self.state.log_execution(step, result)
                except Exception as exc:
                    logger.exception("Failed to log workflow execution for agent %s", agent_name)
                    errors.append({
                        "error": str(exc),
                        "error_type": type(exc).__name__,
                        "step": step,
                        "stage": "state_logging",
                    })
        return {
            "goal": workflow.get("goal"),
            "results": results,
            "errors": errors,
            "status": "failed" if errors else "completed",
        }
