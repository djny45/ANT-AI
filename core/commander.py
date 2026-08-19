"""ANT AI Commander - main orchestration engine."""

from ant_common import Registry


class ANTCommander:
    def __init__(self, name="ANT"):
        self.name = name
        self._registry = Registry()

    @property
    def agents(self):
        return self._registry.mapping

    def register_agent(self, agent_name, agent):
        self._registry.register(agent_name, agent)

    def assign_task(self, task):
        return {
            "task": task,
            "status": "planned",
            "agents": self._registry.names()
        }

    def run(self, task):
        return self.assign_task(task)
