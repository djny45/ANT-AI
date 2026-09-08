"""Experimental web bridge for connecting a website to ANT.

Prototype only. This layer is intentionally thin and does not replace ANT core.
"""

from datetime import datetime


def run_agent_task(task: str) -> dict:
    return {
        "task": task,
        "status": "received",
        "timestamp": datetime.utcnow().isoformat(),
        "message": "ANT experiment bridge received the task"
    }


if __name__ == "__main__":
    print(run_agent_task("test"))
