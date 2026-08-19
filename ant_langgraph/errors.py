"""Error types raised by the ANT AI workflow graph layer."""


class WorkflowError(Exception):
    """Base class for workflow execution failures."""


class UnknownNodeError(WorkflowError):
    """Raised when the graph is asked to run a node that is not registered."""


class NodeExecutionError(WorkflowError):
    """Raised when a graph node raises, preserving the node name and cause."""

    def __init__(self, node: str, cause: BaseException):
        super().__init__(f"Node '{node}' failed: {type(cause).__name__}: {cause}")
        self.node = node
        self.cause = cause
