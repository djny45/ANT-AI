class Planner:
    def create_plan(self, goal: str):
        return [
            {"task": goal, "status": "pending"}
        ]
