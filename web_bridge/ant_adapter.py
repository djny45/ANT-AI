"""Adapter layer between web bridge and existing ANT modules.

Kept separate to avoid modifying the existing runtime during experiments.
"""


def execute_with_ant(task: str):
    # Future connection point to existing ANT autonomy/runtime modules.
    return {
        "task": task,
        "adapter": "ready",
        "execution": "pending runtime binding"
    }
