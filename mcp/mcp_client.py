"""ANT AI Model Context Protocol client foundation."""

from ant_common import Registry


class MCPClient:
    def __init__(self):
        self._registry = Registry()

    @property
    def tools(self):
        return self._registry.mapping

    def register_tool(self, name, tool):
        self._registry.register(name, tool)

    def execute(self, name, payload):
        tool = self._registry.get(name)
        if tool is None:
            return {"error": "tool not found"}
        return tool(payload)
