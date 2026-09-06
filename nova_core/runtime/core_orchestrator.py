"""
NOVA Core v0.8
Core orchestration layer.

Connects runtime, agents, memory, and learning components
into one execution path.
"""


class CoreOrchestrator:
    def __init__(self, agent, memory, learning):
        self.agent = agent
        self.memory = memory
        self.learning = learning

    def run(self, objective):
        previous = self.memory.retrieve(objective)
        result = self.agent.execute(objective, previous)
        self.memory.store(objective, result)
        self.learning.evaluate(result)

        return {
            "objective": objective,
            "result": result,
            "status": "completed"
        }
