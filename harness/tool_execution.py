"""ANT AI Harness controlled tool execution layer.

Provides validated execution boundary between orchestration
and registered external capabilities.
"""


class ToolExecutionController:
    def __init__(self, registry, permissions=None):
        self.registry = registry
        self.permissions = permissions

    def execute(self, name, payload=None):
        if self.permissions is not None:
            if not self.permissions.is_allowed(name):
                return {
                    "status": "blocked",
                    "tool": name,
                    "error": "permission_denied",
                }

        tool = self.registry.get(name)

        if tool is None:
            return {
                "status": "failed",
                "error": "tool_not_found",
            }

        try:
            result = tool(payload)
            return {
                "status": "completed",
                "tool": name,
                "result": result,
            }
        except Exception as error:
            return {
                "status": "failed",
                "tool": name,
                "error": str(error),
            }
