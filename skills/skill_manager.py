"""ANT AI skill lifecycle manager."""

from ant_common import Registry


class SkillManager:
    def __init__(self):
        self._registry = Registry()

    @property
    def skills(self):
        return self._registry.mapping

    def register(self, name, skill):
        self._registry.register(name, skill)

    def list_skills(self):
        return self._registry.names()

    def activate(self, name):
        if name in self._registry:
            return {"skill": name, "active": True}
        return {"error": "skill not found"}
