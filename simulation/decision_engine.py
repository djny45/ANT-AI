"""ANT AI decision selection engine."""

class DecisionEngine:
    def decide(self, options):
        return {
            "selected": options[0] if options else None,
            "requires_validation": True
        }
