class DashboardAPI:
    def status(self, agents=None):
        return {
            "agents": agents or [],
            "status": "online"
        }

    def metrics(self):
        return {
            "tasks": 0,
            "errors": 0
        }
