"""ANT AI skill registry."""

from ant_common import keyword_filter


class SkillRegistry:
    def __init__(self):
        self.registry = []

    def add(self, skill):
        self.registry.append(skill)

    def search(self, keyword):
        return keyword_filter(self.registry, keyword)
