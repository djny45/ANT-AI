"""Policy layer for selecting learning actions."""

class LearningPolicy:
    def choose(self, feedback):
        return "adapt" if feedback else "retain"
