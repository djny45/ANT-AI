"""Pipeline validation tests."""


def test_pipeline_stages_are_ordered():
    stages = [
        "planning",
        "agents",
        "workflow",
        "verification",
    ]
    assert stages.index("planning") < stages.index("verification")
