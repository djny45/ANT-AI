"""ANT Runtime Goal Connector

Adapter layer for connecting the runtime pipeline with goal processing.
"""


class GoalConnector:
    def __init__(self, goal_engine=None):
        self.goal_engine = goal_engine

    def process(self, goal):
        if self.goal_engine:
            return self.goal_engine.process(goal)
        return {"goal": goal, "status": "received"}
