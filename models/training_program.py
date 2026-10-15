class Exercise:
    def __init__(self, name, sets, reps, rest_seconds, description=""):
        self.name = str(name).strip()
        self.sets = int(sets)
        self.reps = int(reps)
        self.rest_seconds = int(rest_seconds)
        self.description = str(description).strip()