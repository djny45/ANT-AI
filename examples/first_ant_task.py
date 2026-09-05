"""
First ANT-AI runtime execution example.

Demonstrates the intended execution flow:
Goal -> Runtime -> Planning -> Agent -> Result
"""

from runtime.ant_runtime import ANTRuntime


def main():
    runtime = ANTRuntime()

    task = {
        "goal": "Analyze a software architecture",
        "priority": "normal"
    }

    result = runtime.execute(task)

    print("ANT Result:")
    print(result)


if __name__ == "__main__":
    main()
