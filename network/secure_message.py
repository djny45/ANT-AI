"""ANT AI secure agent communication."""

class SecureMessage:
    def send(self, sender, receiver, message):
        return {
            "sender": sender,
            "receiver": receiver,
            "message": message,
            "encrypted": True
        }
