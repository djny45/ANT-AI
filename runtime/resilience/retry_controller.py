"""ANT Runtime retry controller."""


class RetryController:
    def __init__(self, max_retries=3):
        self.max_retries = max_retries

    def should_retry(self, attempt: int) -> bool:
        return attempt < self.max_retries

    def execute_with_retry(self, operation):
        last_error = None
        for attempt in range(self.max_retries):
            try:
                return operation()
            except Exception as error:
                last_error = error
        raise last_error
