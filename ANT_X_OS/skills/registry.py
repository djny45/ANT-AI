"""Registry for skills: register, find, list."""
from typing import List, Optional

from ant_common import Registry, keyword_match

from .base_skill import Skill


class SkillRegistry:
    _instance = None

    def __init__(self):
        self._registry: Registry[Skill] = Registry()

    @classmethod
    def instance(cls):
        if cls._instance is None:
            cls._instance = SkillRegistry()
        return cls._instance

    def register(self, skill: Skill):
        self._registry.register(skill.name, skill)

    def get(self, name: str) -> Optional[Skill]:
        return self._registry.get(name)

    def search(self, query: str) -> List[Skill]:
        return [
            s for s in self._registry.values()
            if keyword_match(s.name, query) or keyword_match(s.description, query)
        ]

    def list(self) -> List[Skill]:
        return self._registry.values()

    def clear(self):
        self._registry.clear()

    # helpers for dashboard / introspection
    def active_skills(self) -> List[str]:
        return self._registry.names()


# convenience
registry = SkillRegistry.instance()
