class Executor:
    def execute(self, task):
        try:
            return {"success": True, "result": task}
        except Exception as error:
            return {"success": False, "error": str(error)}
