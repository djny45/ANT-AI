class ANTXRuntime:
    def __init__(self, master_agent, memory, tools):
        self.master_agent = master_agent
        self.memory = memory
        self.tools = tools

    def execute(self, goal):
        plan = self.master_agent.delegate(goal)
        self.memory.store(str(plan), {"goal": goal})
        return plan
