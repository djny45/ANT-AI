from datetime import datetime

class ActivityLogger:
    def log(self, event):
        return {
            "time": datetime.utcnow().isoformat(),
            "event": event
        }
