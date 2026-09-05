"""ANT Runtime integration validator.

Checks that core runtime dependencies are available before execution.
"""


class IntegrationValidator:
    def __init__(self, services=None):
        self.services = services or {}

    def validate(self):
        required = ["planner", "agents", "workflow"]
        missing = [name for name in required if name not in self.services]
        return {
            "ready": len(missing) == 0,
            "missing": missing,
        }
