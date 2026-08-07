import pytest
from ANT_X_OS.skills.registry import registry
from ANT_X_OS.skills.loader import load_builtin_skills


def setup_module():
    registry.clear()
    load_builtin_skills()


def test_registry_lists_skills():
    skills = registry.list()
    assert len(skills) >= 5


def test_registry_get():
    s = registry.get("Coding Skill")
    assert s is not None
