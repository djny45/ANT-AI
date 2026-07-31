class MCPExecutor:
    def __init__(self):
        self.tools = {}

    def register(self, name, tool):
        self.tools[name] = tool

    def execute(self, name, payload):
        if name not in self.tools:
            return {"error": "tool unavailable"}
        return self.tools[name](payload)
