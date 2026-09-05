"""ANT tool selection layer.

Selects execution capabilities based on task requirements.
"""


class ToolSelector:
    def select(self, goal, capabilities):
        if not capabilities:
            return None
        return capabilities[0]
