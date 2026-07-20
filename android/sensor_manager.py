"""ANT AI Android sensor interface."""

class SensorManager:
    def read(self, sensor):
        return {
            "sensor": sensor,
            "value": None
        }
