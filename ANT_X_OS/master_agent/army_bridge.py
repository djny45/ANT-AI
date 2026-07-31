class MasterAgentBridge:
    def __init__(self, army):
        self.army = army

    def delegate(self, goal):
        return self.army.assign(goal)
