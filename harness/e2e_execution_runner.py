"""
ANT AI end-to-end execution runner.

Provides a lightweight verification entry point for the Harness lifecycle.
"""


def validate_execution_flow(steps):
    required = [
        "request",
        "validation",
        "orchestration",
        "runtime",
        "memory",
        "tools",
        "telemetry",
        "result",
    ]

    return all(step in steps for step in required)
