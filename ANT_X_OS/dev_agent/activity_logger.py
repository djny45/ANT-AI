from ant_common import utc_timestamp

class ActivityLogger:
    def log(self, event):
        return {
            "time": utc_timestamp(),
            "event": event
        }
