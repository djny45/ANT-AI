"""NOVA Core v0.7 demonstration runner.

Demonstrates the intended minimal cognitive loop:
Input -> Execution -> Memory -> Feedback -> Result
"""

from datetime import datetime


def run_demo(objective: str):
    print("NOVA CORE ONLINE")
    print("Loading memory...")
    print("Activating agent...")
    print(f"Processing objective: {objective}")

    experience = {
        "objective": objective,
        "timestamp": datetime.utcnow().isoformat(),
        "status": "completed",
    }

    print("Saving experience...")
    print("Updating learning feedback...")
    print("\nRESULT:")
    print(experience)


if __name__ == "__main__":
    run_demo("test task")
