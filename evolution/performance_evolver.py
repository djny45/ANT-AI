"""ANT AI performance improvement system."""

class PerformanceEvolver:
    def compare(self, old_score, new_score):
        return {
            "improvement": new_score - old_score,
            "keep": new_score > old_score
        }
