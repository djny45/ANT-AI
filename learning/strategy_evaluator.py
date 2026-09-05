"""Strategy evaluation foundation."""

class StrategyEvaluator:
    def score(self, strategy, outcome):
        return 1 if outcome else 0
