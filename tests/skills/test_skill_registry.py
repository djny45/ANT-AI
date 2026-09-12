from skills.skill_registry import SkillRegistry


def test_registry_add_and_search():
    registry = SkillRegistry()
    registry.add("Coding Skill")
    registry.add("Review Skill")
    registry.add("Testing Skill")

    assert registry.search("coding") == ["Coding Skill"]
    assert registry.search("skill") == ["Coding Skill", "Review Skill", "Testing Skill"]


def test_registry_empty_search():
    registry = SkillRegistry()
    registry.add("Research Skill")
    assert registry.search("missing") == []
