"""ANT runtime module loader.

Provides controlled loading hooks for existing ANT subsystems.
"""


class ModuleLoader:
    def __init__(self):
        self.modules = {}

    def register(self, name, module):
        self.modules[name] = module

    def get(self, name):
        return self.modules.get(name)

    def available_modules(self):
        return list(self.modules.keys())
