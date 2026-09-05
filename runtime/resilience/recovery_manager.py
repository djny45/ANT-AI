"""Recovery coordination layer for ANT runtime."""


class RecoveryManager:
    def __init__(self, retry_controller=None, exception_manager=None):
        self.retry_controller = retry_controller
        self.exception_manager = exception_manager

    def recover(self, error, context=None):
        if self.exception_manager:
            self.exception_manager.capture(error, context)

        if self.retry_controller:
            return self.retry_controller.retry(context)

        return {
            "recovered": False,
            "error": str(error),
        }
