"""ANT AI external API connector."""

class APIConnector:
    def connect(self, name, endpoint):
        return {
            "name": name,
            "endpoint": endpoint,
            "status": "connected"
        }
