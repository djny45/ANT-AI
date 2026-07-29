class RetryManager:
    def __init__(self, limit=3):
        self.limit = limit

    def should_retry(self, attempt):
        return attempt < self.limit
