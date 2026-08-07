from ANT_X_OS.skills.base_skill import BaseSkill


def test_skill_validation_default():
    s = BaseSkill("T", "D", ["r1"])
    assert not s.validate({})
    assert s.validate({"repo": "x"})
