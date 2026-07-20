"""ANT swarm communication protocol."""

class AgentCommunication:
    def send(self, sender, receiver, message):
        return {
            "from": sender,
            "to": receiver,
            "message": message
        }
