"""ANT AI API rate limiting."""

import time

class RateLimiter:
    def __init__(self, max_requests=20):
        self.max_requests = max_requests
        self.requests = []

    def allow(self):
        now = time.time()
        self.requests = [r for r in self.requests if now - r < 60]
        if len(self.requests) >= self.max_requests:
            return False
        self.requests.append(now)
        return True
