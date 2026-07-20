"""ANT AI core operating kernel."""

class ANTKernal:
    def __init__(self):
        self.modules = {}

    def register(self, name, module):
        self.modules[name] = module

    def status(self):
        return list(self.modules.keys())
