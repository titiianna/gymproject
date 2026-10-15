from models.training_program import Exercise, TrainingProgram


class CoachService:
    """Business logic for the coach panel"""

    @staticmethod
    def _class_id(class_obj):
        return str(getattr(class_obj, "class_id", ""))

    @staticmethod
    def _find_class(class_id, classes_list):
        wanted = str(class_id)
        for class_obj in classes_list:
            if CoachService._class_id(class_obj) == wanted:
                return class_obj
        return None
    
    @staticmethod
    def _program_key(class_id, member_username):
        return f"{class_id}:{member_username}"
        
        
    @staticmethod
    def _is_active_member_of_class(class_obj, member_username, member):
        has_active_member = getattr(class_obj, "has_active_member", None)
        if callable(has_active_member):
            try:
                return bool(has_active_member(member_username))
            except (TypeError, AttributeError):
                pass

        enrollments = getattr(class_obj, "enrollments", None)
        if isinstance(enrollments, dict):
            enrollment = enrollments.get(member_username)
            if enrollment is not None:
                return bool(getattr(enrollment, "is_active", False))
        elif isinstance(enrollments, (list, tuple)):
            for enrollment in enrollments:
                if getattr(enrollment, "username", None) == member_username:
                    return bool(getattr(enrollment, "is_active", False))

        registered_classes = getattr(member, "registered_classes", [])
        return CoachService._class_id(class_obj) in {
            str(value) for value in (registered_classes or [])
        }   
        
    @staticmethod
    def get_coach_classes(coach_username, classes_list):
        """Return the classes assigned to a coach"""
        return [
            class_obj 
            for class_obj in classes_list
            if getattr(class_obj, "coach_username", None) == coach_username
            ]
    
    @staticmethod
    def get_class_members(coach_username, class_id, classes_list, users_dict):
        """Return (ok, msg, members) for active members of a class"""
        class_obj = CoachService._find_class(class_id, classes_list)
        if class_obj is None:
            return False, "class not found", []
    
        if getattr(class_obj, "coach_username", None) != coach_username:
            return False, "You do not have access to this class", []
    
        members = []
        for username, user in users_dict.items():
            if getattr(user, "role", None) != "member":
                continue
            if not getattr(user, "is_active", False):
                continue
            if CoachService._is_active_member_of_class(class_obj, username, user):
                members.append(user)
    
            return True, "Active class members retrieved successfully", members
    @staticmethod
    def validate_exercise(exercise):
        """ Validate exercise data and return (ok, msg) """
        if isinstance(exercise, dict):
            try:
                exercise = Exercise.from_dict(exercise)
            except (TypeError, ValueError, KeyError):
                return False, "Exercise data is incomplete or invalid"
    
        required_attrs = ("name", "sets", "reps", "rest_seconds")
        if not all(hasattr(exercise, attr) for attr in required_attrs):
            return False, "Invalid exercise data structure."
    
        if not str(exercise.name).strip():
            return False, "Exercise name cannot be emty"
    
        try:
            sets = int(exercise.sets)
            reps = int(exercise.reps)
            rest = int(exercise.rest_seconds)
        except (TypeError, ValueError):
            return False, "Sets, reps, and rest time must be integers."
    
        if sets <= 0:
            return False, "Sets must be greater than zero"
        if reps <= 0:
            return False, "Reps must be greater than zero"
        if rest < 0:
            return False, "Rest time cannot be negative"
    
        return True, "Exercise data is valid"
    
    @staticmethod
    def add_training_program(
        class_id, 
        member_username, 
        exercises, 
        coach_username,
        classes_list, 
        users_dict, 
        programs_dict
    ):
        """Create a training program for an active member of the coach's class"""
        class_obj = CoachService._find_class(class_id, classes_list)
        if class_obj is None:
            return False, "Class not found"
    
        if getattr(class_obj, "coach_username", None) != coach_username:
            return False, "You can only create programs for your own classes"
    
        member = users_dict.get(member_username)
        if member is None or getattr(member, "role", None) != "member":
            return False, "member not found"
        if not getattr(member, "is_active", False):
            return False, "the member account is inactive"
    
        if not CoachService._is_active_member_of_class(class_obj, member_username, member):
            return False, "The member is not actively enrolled in this class"
    
        if not exercises:
            return False, "A training program must contain at least one exercise"
    
        valid_exercises = []
        for exercise in exercises:
            ok, msg = CoachService.validate_exercise(exercise)
            if not ok:
                return False, msg
            if isinstance(exercise, dict):
                exercise = Exercise.from_dict(exercise)
            valid_exercises.append(exercise)
    
        key = CoachService._program_key(class_id, member_username)
        if key in programs_dict:
            return False, 
        "A program already exists for this member in this class. "
        "Use add_exercise instead.",
    
        programs_dict[key] = TrainingProgram(
            class_id=class_id,
            member_username=member_username,
            coach_username=coach_username,
            exercises=valid_exercises,
        )
        return True, "Training program created successfully"
    
    @staticmethod
    def add_exercise(
        class_id, member_username, exercise, coach_username,
        classes_list, programs_dict
    ):
        """Add an exercise to an existing training program."""
        class_obj = CoachService._find_class(class_id, classes_list)
        if class_obj is None:
            return False, "class not found"
        if getattr(class_obj, "coach_username", None) != coach_username:
            return False, "You can only modify programs for your own classes"
    
        ok, msg = CoachService.validate_exercise(exercise)
        if not ok:
            return False, msg
        if isinstance(exercise, dict):
            exercise = Exercise.from_dict(exercise)
    
        key = CoachService._program_key(class_id, member_username)
        program = programs_dict.get(key)
        if program is None:
            return False, "No training program exists for this member"
        if getattr(program, "coach_username", None) != coach_username:
            return False, "You do not have permission to modify this program"
    
        try:
            program.add_exercise(exercise)
        except (TypeError, ValueError) as error:
            return False, f"Failed to add exercise {error}"
        return True, "Exercise added successfully"
    
    @staticmethod
    def edit_exercise(
        class_id, member_username, index, new_data, coach_username,
        classes_list, programs_dict
    ):
        """Edit an exercise using a zero-based index."""
        class_obj = CoachService._find_class(class_id, classes_list)
        if class_obj is None:
            return False, "class not found "
        if getattr(class_obj, "coach_username", None) != coach_username:
            return False, "You can only modify programs for your own classes"
    
        key = CoachService._program_key(class_id, member_username)
        program = programs_dict.get(key)
        if program is None:
            return False, "training program not found"
        if getattr(program, "coach_username", None) != coach_username:
            return False, "You do not have permission to modify this program"
    
        try:
            index = int(index)
        except (TypeError, ValueError):
            return False, "Invalid exercise index"
        if index < 0 or index >= len(program.exercises):
            return False, "Exercise index is out of range"
    
        old = program.exercises[index]

        if isinstance(new_data, Exercise):
            new_data = new_data.to_dict()

        if not isinstance(new_data, dict):
            return False, "New exercise data is invalid."

        merged = old.to_dict()

        for key in merged:
            if new_data.get(key) is not None:
                merged[key] = new_data[key]

        try:
            new_exercise = Exercise.from_dict(merged)
        except (TypeError, ValueError, KeyError):
            return False, "New exercise data is invalid."

        ok, msg = CoachService.validate_exercise(new_exercise)

        if not ok:
            return False, msg
    
        program.exercises[index] = new_exercise
        return True, "Exercise updated successfully"
    
    @staticmethod
    def get_program(
        coach_username, class_id, member_username, classes_list, programs_dict
    ):
        """Return (ok, msg, TrainingProgram or None)"""
        class_obj = CoachService._find_class(class_id, classes_list)
        if class_obj is None:
            return False, "class not found", None
        if getattr(class_obj, "coach_username", None) != coach_username:
            return False, "You do not have permission to view this class", None
    
        key = CoachService._program_key(class_id, member_username)
        program = programs_dict.get(key)
        if program is None:
            return True, "No training program exists for this member yet", None
        if getattr(program, "coach_username", None) != coach_username:
            return False, "You do not have permission to view this program", None
    
        return True, "Training program retrieved successfully", program
    