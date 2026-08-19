from ant_common import Registry


class MCPExecutor:
    def __init__(self):
        self._registry = Registry()

    @property
    def tools(self):
        return self._registry.mapping

    def register(self, name, tool):
        self._registry.register(name, tool)

    def execute(self, name, request):
        tool = self._registry.get(name)
        if tool is None:
            return {"error": "tool unavailable"}
        return tool(request)
