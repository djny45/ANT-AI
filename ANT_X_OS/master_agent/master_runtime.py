class MasterAgentRuntime:
    def __init__(self, planner, registry, evaluator=None):
        self.planner = planner
        self.registry = registry
        self.evaluator = evaluator

    def run(self, goal):
        tasks = self.planner.plan(goal)
        results = []
        for task in tasks:
            agent = self.registry.get(task.get("agent"))
            if agent:
                results.append(agent.run(task))
        if self.evaluator:
            return self.evaluator.evaluate(goal, results)
        return results
