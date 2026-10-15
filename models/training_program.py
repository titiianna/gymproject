class Exercise:
    def __init__(self, name, sets, reps, rest_seconds, description=""):
        self.name = str(name).strip()
        self.sets = int(sets)
        self.reps = int(reps)
        self.rest_seconds = int(rest_seconds)
        self.description = str(description).strip()
        
    def to_dict(self):
        return {
            "name": self.name,
            "sets": self.sets,
            "reps": self.reps,
            "rest_seconds": self.rest_seconds,
            "description": self.description,
        }
        
    @classmethod
    def from_dict(cls, data):
        return cls(
            name=data.get("name", ""),
            sets=data.get("sets", 0),
            reps=data.get("reps", 0),
            rest_seconds=data.get("rest_seconds", 0),
            description=data.get("description", ""),
        )
        
class TrainingProgram:
    def __init__(self, class_id, member_username, coach_username, exercises=None):
        self.class_id = str(class_id)
        self.member_username = str(member_username)
        self.coach_username = str(coach_username)
        self.exercises = list(exercises) if exercises is not None else []

    