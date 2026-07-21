"""ANT web-to-app integration router."""

class WebAppIntegrationRouter:
    def route(self, project):
        return {
            "project": project,
            "pipeline": [
                "analysis",
                "generation",
                "simulation",
                "testing",
                "deployment"
            ]
        }
