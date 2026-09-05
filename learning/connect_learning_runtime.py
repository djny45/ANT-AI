"""Bridge learning systems with runtime execution."""

class LearningRuntimeConnector:
    def __init__(self, learner=None):
        self.learner = learner

    def process_execution(self, execution_result):
        if self.learner and hasattr(self.learner, "learn"):
            return self.learner.learn(execution_result)
        return {"status": "learning_pending", "result": execution_result}
