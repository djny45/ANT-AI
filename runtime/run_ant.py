"""
ANT-AI Unified Runtime Launcher

Entry point for starting the ANT execution pipeline.
"""

from runtime.bootstrap import bootstrap_runtime
from runtime.execution_context import ExecutionContext


def run_ant(goal: str):
    runtime = bootstrap_runtime()

    context = ExecutionContext(
        goal=goal,
        metadata={"source": "run_ant"}
    )

    result = runtime.execute(context)

    return result


if __name__ == "__main__":
    response = run_ant("Analyze a software architecture")
    print(response)
