from skills.skill_registry import SkillRegistry


def test_skill_registry_accepts_valid_skill_values():
    registry = SkillRegistry()
    registry.add("Coding Skill")
    assert registry.search("Coding Skill") == ["Coding Skill"]


def test_skill_registry_does_not_match_unrelated_values():
    registry = SkillRegistry()
    registry.add("Coding Skill")
    assert registry.search("Security Skill") == []
