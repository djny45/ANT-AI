class SecurityManager:
    def __init__(self):
        self.allowed = set()

    def allow(self, action):
        self.allowed.add(action)

    def check(self, action):
        return action in self.allowed
