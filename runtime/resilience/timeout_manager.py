"""ANT Runtime timeout manager."""

import time


class TimeoutManager:
    def __init__(self, timeout_seconds=30):
        self.timeout_seconds = timeout_seconds
        self.started_at = None

    def start(self):
        self.started_at = time.time()

    def expired(self):
        if self.started_at is None:
            return False
        return (time.time() - self.started_at) > self.timeout_seconds
