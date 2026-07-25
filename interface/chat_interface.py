"""ANT AI chat interface."""

class ChatInterface:
    def send(self, message):
        return {
            "input": message,
            "status": "received"
        }
