"""ANT workflow execution bridge.

Connects runtime pipeline with workflow execution.
"""


class WorkflowExecutionBridge:
    def execute_workflow(self, workflow):
        return {"workflow": workflow, "status": "started"}
