"""Experience storage foundation for ANT learning loop."""

class ExperienceStore:
    def __init__(self):
        self.experiences = []

    def record(self, experience):
        self.experiences.append(experience)

    def all(self):
        return self.experiences
