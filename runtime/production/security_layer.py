"""ANT production security layer foundation."""


class SecurityLayer:
    def __init__(self):
        self.policies = {}

    def register_policy(self, name, value):
        self.policies[name] = value

    def validate(self, context=None):
        return True
