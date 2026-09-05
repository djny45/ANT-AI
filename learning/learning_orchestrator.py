"""Learning loop orchestration foundation."""

class LearningOrchestrator:
    def __init__(self, store, feedback):
        self.store = store
        self.feedback = feedback

    def learn(self, experience):
        evaluation = self.feedback.evaluate(experience)
        self.store.record({"experience": experience, "evaluation": evaluation})
        return evaluation
