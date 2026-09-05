"""
ANT Runtime Dependency Manager

Loads and manages runtime components.
"""


class DependencyManager:
    def __init__(self, container):
        self.container = container

    def add_dependency(self, name, component):
        self.container.register(name, component)

    def get_dependency(self, name):
        return self.container.resolve(name)
