"""ANT production API gateway foundation."""


class APIGateway:
    def __init__(self, orchestrator=None):
        self.orchestrator = orchestrator

    def handle_request(self, goal):
        if self.orchestrator:
            return self.orchestrator.execute(goal)
        return {"goal": goal, "status": "received"}
