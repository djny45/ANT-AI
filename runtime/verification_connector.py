"""ANT Runtime verification connector.

Provides a bridge between the execution pipeline and verification systems.
"""


class VerificationConnector:
    def __init__(self, verifier=None):
        self.verifier = verifier

    def verify(self, result, context=None):
        if self.verifier:
            return self.verifier(result, context)
        return {
            "verified": True,
            "result": result,
        }
