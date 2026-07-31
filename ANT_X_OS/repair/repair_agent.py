class RepairAgent:
    def analyze(self, error):
        return {"error": error, "action": "analyze"}

    def propose_fix(self, issue):
        return {"patch": None, "requires_validation": True}
