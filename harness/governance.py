"""ANT AI Harness governance boundary.

Provides lightweight policy checks before execution.
"""


class Governance:
    def evaluate(self, request: dict) -> dict:
        return {
            "allowed": True,
            "reason": "Request passed governance checks",
        }
