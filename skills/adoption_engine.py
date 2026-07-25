"""ANT AI skill adoption decision engine."""

class AdoptionEngine:
    def decide(self, security_result, test_result):
        if security_result == "pass" and test_result == "pass":
            return "adopt"
        return "reject"
