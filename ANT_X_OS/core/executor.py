import logging

logger = logging.getLogger(__name__)


class Executor:
    def execute(self, task):
        if not callable(task):
            return {"success": True, "result": task}
        try:
            return {"success": True, "result": task()}
        except Exception as error:
            logger.exception("Task execution failed")
            return {"success": False, "error": str(error), "error_type": type(error).__name__}
