from typing import Any, Callable, Dict


class WorkflowExecutor:
    """Adapter boundary between the graph and ANT_X_OS agent implementations."""

    def __init__(self, handlers: Dict[str, Callable[..., Any]] | None = None):
        self.handlers = handlers or {}

    def register(self, agent: str, handler: Callable[..., Any]) -> None:
        self.handlers[agent] = handler

    def execute(self, agent: str, task: Dict[str, Any], context: Dict[str, Any]) -> Any:
        handler = self.handlers.get(agent)
        if handler is None:
            raise KeyError(f"No handler registered for agent: {agent}")
        return handler(task=task, context=context)
