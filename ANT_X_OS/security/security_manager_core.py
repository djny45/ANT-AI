class SecurityManager:
    def __init__(self):
        self.permissions = {}

    def allow(self, action):
        self.permissions[action] = True

    def check(self, action):
        return self.permissions.get(action, False)
