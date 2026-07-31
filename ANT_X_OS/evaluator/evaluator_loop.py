class Evaluator:
    def evaluate(self, task, result):
        return {
            "task": task,
            "success": bool(result),
            "score": 1 if result else 0
        }

    def improve(self, evaluation):
        return {"learning_saved": True, "evaluation": evaluation}
