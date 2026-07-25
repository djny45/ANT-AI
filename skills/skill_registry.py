"""ANT AI skill registry."""

class SkillRegistry:
    def __init__(self):
        self.registry = []

    def add(self, skill):
        self.registry.append(skill)

    def search(self, keyword):
        return [s for s in self.registry if keyword.lower() in str(s).lower()]
