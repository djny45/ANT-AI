"""ANT AI Harness tool permission boundary.

Controls authorization checks before tool execution.
"""


class ToolPermissionManager:
    def __init__(self):
        self.permissions = {}

    def allow(self, tool_name):
        self.permissions[tool_name] = True

    def deny(self, tool_name):
        self.permissions[tool_name] = False

    def can_execute(self, tool_name):
        return self.permissions.get(tool_name, False)
