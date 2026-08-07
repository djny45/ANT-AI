from ANT_X_OS.skills.selector import SkillSelector
from ANT_X_OS.skills.loader import load_builtin_skills
from ANT_X_OS.skills.registry import registry


def test_selector_code_task():
    registry.clear()
    load_builtin_skills()
    sel = SkillSelector(registry)
    skills = sel.select_for_task({"type": "code", "description": "implement feature X"})
    assert "Coding Skill" in skills


def test_selector_bug_task():
    sel = SkillSelector(registry)
    skills = sel.select_for_task({"description": "fix bug causing error"})
    assert "Debugging Skill" in skills
