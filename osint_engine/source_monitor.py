"""ANT OSINT source monitoring."""

class SourceMonitor:
    def check(self, source):
        return {
            "source": source,
            "status": "checked"
        }
