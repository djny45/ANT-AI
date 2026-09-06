"""NOVA Core v0.3 Task Controller
Connects user objectives with agents, memory, and learning components.
"""


class TaskController:
    def __init__(self, agent, memory, learning):
        self.agent = agent
        self.memory = memory
        self.learning = learning

    def run(self, objective):
        context = self.memory.retrieve(objective)
        result = self.agent.execute(objective, context)
        self.memory.store(objective, result)
        self.learning.evaluate(result)
        return result
