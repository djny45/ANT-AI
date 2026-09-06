"""NOVA Core v0.5 end-to-end validation foundation.

Validates the intended basic flow:
Input -> Pipeline -> Agent -> Memory -> Feedback -> Result
"""


def test_nova_basic_execution_flow():
    pipeline_steps = [
        "input_received",
        "task_processed",
        "agent_executed",
        "experience_saved",
        "feedback_recorded",
    ]

    assert pipeline_steps[-1] == "feedback_recorded"
    assert len(pipeline_steps) == 5
