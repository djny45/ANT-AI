class ProductionRuntime:
    def __init__(self, master_agent, agent_registry, tools, memory):
        self.master_agent = master_agent
        self.agent_registry = agent_registry
        self.tools = tools
        self.memory = memory

    def execute_goal(self, goal):
        context = {"goal": goal}
        self.memory.store(str(context), {"type": "runtime"})
        return self.master_agent.run(goal)
