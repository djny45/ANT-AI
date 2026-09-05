"""
ANT Runtime Service Container

Central dependency registry for connecting ANT subsystems.
"""


class ServiceContainer:
    def __init__(self):
        self.services = {}

    def register(self, name, service):
        self.services[name] = service

    def resolve(self, name):
        return self.services.get(name)

    def available_services(self):
        return list(self.services.keys())
