import logging

logger = logging.getLogger(__name__)


class MCPExecutor:
    def __init__(self):
        self.tools = {}
        self.permissions = {}

    def register(self, name, tool, permission="safe"):
        self.tools[name] = tool
        self.permissions[name] = permission

    def execute(self, name, payload, approved=False):
        if name not in self.tools:
            logger.warning("MCP tool unavailable: %s", name)
            return {"success": False, "error": "tool unavailable", "error_type": "ToolUnavailable"}

        if self.permissions.get(name) != "safe" and not approved:
            logger.warning("MCP tool %s requires approval but none was given", name)
            return {"success": False, "error": "permission required", "error_type": "PermissionRequired"}

        try:
            return {"success": True, "result": self.tools[name](payload)}
        except Exception as error:
            logger.exception("MCP tool %s raised an exception", name)
            return {
                "success": False,
                "error": str(error),
                "error_type": type(error).__name__,
                "tool": name,
            }
