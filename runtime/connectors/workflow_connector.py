"""ANT Runtime Workflow Connector

Adapter for workflow execution.
"""


class WorkflowConnector:
    def __init__(self, workflow_runtime=None):
        self.workflow_runtime = workflow_runtime

    def execute(self, workflow):
        if self.workflow_runtime:
            return self.workflow_runtime.execute(workflow)
        return {"workflow": workflow, "status": "completed"}
