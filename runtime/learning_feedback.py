"""ANT learning feedback layer."""


class LearningFeedback:
    def __init__(self):
        self.feedback = []

    def record(self, signal):
        self.feedback.append(signal)

    def history(self):
        return self.feedback
