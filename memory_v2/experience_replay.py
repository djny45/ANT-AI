"""ANT AI learns from previous missions."""

class ExperienceReplay:
    def __init__(self):
        self.experiences = []

    def store(self, mission, result):
        self.experiences.append({"mission": mission, "result": result})

    def recall(self):
        return self.experiences
