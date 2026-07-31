class MasterArmyBridge:
    def __init__(self, army):
        self.army = army

    def delegate(self, goal):
        return self.army.assign(goal)

    def report(self, result):
        return {"master_received": True, "result": result}
