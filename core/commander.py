"""ANT AI Commander - main orchestration engine."""

class ANTCommander:
    def __init__(self, name="ANT"):
        self.name = name
        self.agents = {}

    def register_agent(self, agent_name, agent):
        self.agents[agent_name] = agent

    def assign_task(self, task):
        return {
            "task": task,
            "status": "planned",
            "agents": list(self.agents.keys())
        }

    def run(self, task):
        return self.assign_task(task)
