class Evaluator:
    def evaluate(self, result):
        return {
            "success": result.get("success", False),
            "quality": "verified" if result.get("success") else "failed"
        }
