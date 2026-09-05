"""Factory for constructing ANT runtime components."""


class RuntimeFactory:
    def create(self, goal=None):
        return {
            "runtime": "ANT",
            "goal": goal,
            "status": "initialized",
        }
