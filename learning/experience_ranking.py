"""Experience ranking foundation for ANT-AI learning."""

class ExperienceRanker:
    def rank(self, experiences):
        return sorted(experiences, key=lambda x: x.get("score", 0), reverse=True)
