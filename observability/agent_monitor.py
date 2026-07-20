"""ANT AI agent monitoring."""

class AgentMonitor:
    def __init__(self):
        self.logs = []

    def record(self, agent, action, result):
        self.logs.append({
            "agent": agent,
            "action": action,
            "result": result
        })

    def history(self):
        return self.logs
