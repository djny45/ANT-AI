"""ANT OSINT source evaluation layer."""

class SourceEvaluator:
    def evaluate(self, source):
        return {
            "source": source,
            "status": "needs_review"
        }
