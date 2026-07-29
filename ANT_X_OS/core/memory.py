class Memory:
    def __init__(self):
        self.short_term = []
        self.long_term = []

    def store(self, item, permanent=False):
        if permanent:
            self.long_term.append(item)
        else:
            self.short_term.append(item)

    def retrieve(self):
        return self.short_term + self.long_term
