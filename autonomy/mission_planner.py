"""ANT AI mission planner."""

class MissionPlanner:
    def plan(self, goal):
        return {
            "goal": goal,
            "steps": [],
            "status": "planned"
        }
