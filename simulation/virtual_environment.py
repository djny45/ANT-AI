"""ANT AI simulation environment."""

class VirtualEnvironment:
    def __init__(self):
        self.state = {}

    def set_state(self, key, value):
        self.state[key] = value

    def observe(self):
        return self.state
