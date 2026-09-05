"""Planner adapter for ANT Runtime integration."""

class PlannerAdapter:
    def __init__(self, planner=None):
        self.planner = planner

    def create_plan(self, goal):
        if self.planner and hasattr(self.planner, "plan"):
            return self.planner.plan(goal)
        return {"goal": goal, "status": "planned"}
