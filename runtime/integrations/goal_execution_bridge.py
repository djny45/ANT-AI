"""ANT goal execution bridge.

Adapter layer between runtime and planning components.
"""


class GoalExecutionBridge:
    def execute_goal(self, goal):
        return {"goal": goal, "status": "queued"}
