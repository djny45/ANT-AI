"""ANT AI internal event bus."""

class EventBus:
    def __init__(self):
        self.events = []

    def publish(self, event):
        self.events.append(event)

    def get_events(self):
        return self.events

    def clear(self):
        self.events = []
