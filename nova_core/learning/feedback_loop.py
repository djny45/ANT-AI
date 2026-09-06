"""NOVA Core v0.2 feedback learning prototype."""


class FeedbackLoop:
    def evaluate(self, result):
        return {
            "result": result,
            "score": 1.0 if result else 0.0,
        }
