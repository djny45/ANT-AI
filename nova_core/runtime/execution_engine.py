"""
NOVA Core v0.6 Execution Engine

Connects the basic runtime pipeline:
Input -> Task -> Agent -> Memory -> Feedback -> Result
"""


class ExecutionEngine:
    def __init__(self, agent, memory, learning):
        self.agent = agent
        self.memory = memory
        self.learning = learning

    def run(self, objective):
        context = self.memory.retrieve(objective)
        result = self.agent.execute(objective, context)
        self.memory.store(objective, result)
        self.learning.evaluate(objective, result)
        return result
