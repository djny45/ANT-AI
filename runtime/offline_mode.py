"""ANT AI offline operation mode."""

class OfflineMode:
    def enable(self):
        return {
            "mode": "offline",
            "cloud": False
        }
