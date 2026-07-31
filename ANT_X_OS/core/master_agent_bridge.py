class MasterAgentBridge:
    def __init__(self, army):
        self.army = army

    def dispatch_goal(self, goal):
        return self.army.assign(goal)
