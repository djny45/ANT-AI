class Sandbox:
    def __init__(self):
        self.allowed = []

    def allow(self, action):
        self.allowed.append(action)

    def execute(self, action, fn, *args):
        if action not in self.allowed:
            raise PermissionError("action blocked")
        return fn(*args)
