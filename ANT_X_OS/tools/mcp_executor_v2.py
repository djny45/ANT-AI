class MCPExecutor:
    def __init__(self):
        self.tools = {}

    def register(self, name, tool):
        self.tools[name] = tool

    def execute(self, name, request):
        tool = self.tools.get(name)
        if tool is None:
            return {"error": "tool unavailable"}
        return tool(request)
