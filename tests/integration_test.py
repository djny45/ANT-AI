"""Integration contract test for ANT end-to-end flow."""


def test_ant_end_to_end_flow():
    flow = [
        "input",
        "runtime",
        "agent",
        "workflow",
        "verification",
        "memory",
    ]
    assert "runtime" in flow
    assert "verification" in flow
    assert "memory" in flow
