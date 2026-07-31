class Evaluator:
    def evaluate(self, task, result):
        return {
            "task": task,
            "success": bool(result),
            "improvement": "store lessons"
        }
