"""ANT AI Model Context Protocol client foundation."""

class MCPClient:
    def __init__(self):
        self.tools = {}

    def register_tool(self, name, tool):
        self.tools[name] = tool

    def execute(self, name, payload):
        if name not in self.tools:
            return {"error": "tool not found"}
        return self.tools[name](payload)
