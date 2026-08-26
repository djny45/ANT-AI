"""ANT AI Harness execution telemetry layer.

Provides structured runtime observability records for execution tracking.
"""


class TelemetryCollector:
    def __init__(self):
        self.events = []

    def record(self, event_type, execution_id, metadata=None):
        event = {
            "event_type": event_type,
            "execution_id": execution_id,
            "metadata": metadata or {},
        }
        self.events.append(event)
        return event

    def list_events(self):
        return self.events
