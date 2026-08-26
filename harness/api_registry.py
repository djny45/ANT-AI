"""ANT AI Harness API route registry.

Central registration point for service endpoints.
"""

from .history_routes import HistoryRoutes
from .health_endpoint import HealthEndpoint


class APIRouteRegistry:
    def __init__(self):
        self.routes = {
            "health": HealthEndpoint(),
            "history": HistoryRoutes(),
        }

    def get_routes(self):
        return self.routes
