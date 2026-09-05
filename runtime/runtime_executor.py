"""
ANT Runtime Executor

Coordinates execution using registered ANT services.
"""


class RuntimeExecutor:
    def __init__(self, container):
        self.container = container

    def execute(self, goal):
        context = {
            "goal": goal,
            "status": "initialized"
        }

        planner = self.container.resolve("planner")
        if planner:
            context["plan"] = planner.plan(goal)

        context["status"] = "completed"
        return context
