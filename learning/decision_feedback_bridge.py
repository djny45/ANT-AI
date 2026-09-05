"""Bridge learning feedback into runtime decision selection."""

class DecisionFeedbackBridge:
    def apply_feedback(self, decision_context, feedback):
        return {**decision_context, "learning_feedback": feedback}
