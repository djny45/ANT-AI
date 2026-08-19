import logging

logger = logging.getLogger(__name__)


class MCPExecutor:
    def __init__(self):
        self.tools = {}

    def register(self, name, tool):
        self.tools[name] = tool

    def execute(self, name, request):
        tool = self.tools.get(name)
        if tool is None:
            logger.warning("MCP tool unavailable: %s", name)
            return {"error": "tool unavailable", "error_type": "ToolUnavailable", "tool": name}
        try:
            return tool(request)
        except Exception as error:
            logger.exception("MCP tool %s raised an exception", name)
            return {"error": str(error), "error_type": type(error).__name__, "tool": name}
