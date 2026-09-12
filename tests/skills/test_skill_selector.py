from skills.skill_registry import SkillRegistry


def test_registry_search_selects_relevant_skill():
    registry = SkillRegistry()
    registry.add("Coding Skill")
    registry.add("Research Skill")
    registry.add("Testing Skill")

    selected = registry.search("code")
    assert selected == ["Coding Skill"]


def test_registry_search_is_case_insensitive():
    registry = SkillRegistry()
    registry.add("Debugging Skill")
    assert registry.search("DEBUG") == ["Debugging Skill"]
