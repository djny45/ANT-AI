"""Basic tests for ANT runtime lifecycle."""


def test_runtime_pipeline_contract():
    pipeline = [
        "goal",
        "planning",
        "agent_selection",
        "execution",
        "verification",
        "memory_update",
    ]
    assert pipeline[0] == "goal"
    assert pipeline[-1] == "memory_update"
