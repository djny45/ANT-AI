class MCPExecutor:
    def __init__(self):
        self.tools = {}
        self.permissions = {}

    def register(self, name, tool, permission="safe"):
        self.tools[name] = tool
        self.permissions[name] = permission

    def execute(self, name, payload, approved=False):
        if name not in self.tools:
            return {"success": False, "error": "tool unavailable"}

        if self.permissions.get(name) != "safe" and not approved:
            return {"success": False, "error": "permission required"}

        try:
            return {"success": True, "result": self.tools[name](payload)}
        except Exception as error:
            return {"success": False, "error": str(error)}
