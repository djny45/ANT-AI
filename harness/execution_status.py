"""
ANT AI Harness execution status tracking.

Provides a lightweight status layer for monitoring
successful, failed, and incomplete executions.
"""


def create_status(state="pending", message="Execution started"):
    return {
        "state": state,
        "message": message,
    }


def success(message="Execution completed"):
    return create_status("completed", message)


def failure(message="Execution failed"):
    return create_status("failed", message)
