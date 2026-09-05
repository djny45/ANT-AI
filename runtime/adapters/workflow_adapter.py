"""Workflow adapter for ANT Runtime integration."""

class WorkflowAdapter:
    def __init__(self, workflow_runtime=None):
        self.workflow_runtime = workflow_runtime

    def execute(self, workflow):
        if self.workflow_runtime and hasattr(self.workflow_runtime, "run"):
            return self.workflow_runtime.run(workflow)
        return {"workflow": workflow, "status": "completed"}
