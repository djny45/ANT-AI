"""Registry for skills: register, find, list."""
from typing import Dict, List, Optional
from .base_skill import Skill, BaseSkill


class SkillRegistry:
    _instance = None

    def __init__(self):
        self._skills: Dict[str, Skill] = {}

    @classmethod
    def instance(cls):
        if cls._instance is None:
            cls._instance = SkillRegistry()
        return cls._instance

    def register(self, skill: Skill):
        self._skills[skill.name] = skill

    def get(self, name: str) -> Optional[Skill]:
        return self._skills.get(name)

    def search(self, query: str) -> List[Skill]:
        q = query.lower()
        return [s for s in self._skills.values() if q in s.name.lower() or q in s.description.lower()]

    def list(self) -> List[Skill]:
        return list(self._skills.values())

    def clear(self):
        self._skills = {}

    # helpers for dashboard / introspection
    def active_skills(self) -> List[str]:
        return [s.name for s in self._skills.values()]


# convenience
registry = SkillRegistry.instance()
