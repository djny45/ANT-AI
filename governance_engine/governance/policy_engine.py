"""ANT AI governance policy engine.

Defines central rules for controlled autonomous actions.
"""


class PolicyEngine:
    def __init__(self):
        self.blocked_actions = {
            "delete_production_data",
            "expose_secrets",
            "disable_security",
        }

    def check(self, action: str) -> bool:
        return action not in self.blocked_actions
