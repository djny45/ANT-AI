"""ANT AI skill lifecycle manager."""

class SkillManager:
    def __init__(self):
        self.skills = {}

    def register(self, name, skill):
        self.skills[name] = skill

    def list_skills(self):
        return list(self.skills.keys())

    def activate(self, name):
        if name in self.skills:
            return {"skill": name, "active": True}
        return {"error": "skill not found"}
