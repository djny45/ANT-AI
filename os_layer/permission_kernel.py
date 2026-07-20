"""ANT AI permission control kernel."""

class PermissionKernel:
    def __init__(self):
        self.permissions = {}

    def grant(self, agent, action):
        self.permissions.setdefault(agent, []).append(action)

    def allowed(self, agent, action):
        return action in self.permissions.get(agent, [])
