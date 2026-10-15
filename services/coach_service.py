from models.training_program import Exercise, TrainingProgram
from utils.decorators import log_action
from utils.validators import Validators


def _key(class_id, member_username):
    return f"{class_id}:{member_username}"


def _get_owned_class(coach_username, class_id, classes_list):
    for c in classes_list:
        if c.class_id == class_id and c.coach_username == coach_username:
            return c
    return None


def _field(item, name, default=None):
    if isinstance(item, dict):
        return item.get(name, default)
    return getattr(item, name, default)


class CoachService:
    @staticmethod
    def get_coach_classes(coach_username, classes_list):
        return [c for c in classes_list if c.coach_username == coach_username]

    @staticmethod
    def get_class_members(coach_username, class_id, classes_list, users_dict):
        cls = _get_owned_class(coach_username, class_id, classes_list)
        if cls is None:
            return False, "This class does not exist or does not belong to you.", []
        members = [users_dict[u] for u in cls.active_member_usernames() if u in users_dict]
        return True, "", members

    @staticmethod
    def _build_exercise(item):
        name = _field(item, "name")
        if not isinstance(name, str) or not name.strip():
            return False, "Exercise name cannot be empty.", None
        sets_, reps = _field(item, "sets"), _field(item, "reps")
        if not Validators.positive_int_validate(sets_):
            return False, "Sets must be an integer greater than zero.", None
        if not Validators.positive_int_validate(reps):
            return False, "Reps must be an integer greater than zero.", None
        rest = _field(item, "rest_seconds")
        if not Validators.non_negative_int_validate(rest):
            return False, "Rest time must be a non-negative integer (seconds).", None
        description = _field(item, "description", "") or ""
        return True, "", Exercise(name.strip(), int(sets_), int(reps), int(rest), str(description))

    @staticmethod
    def validate_exercise(exercise):
        ok, msg, _ = CoachService._build_exercise(exercise)
        return ok, msg

    @staticmethod
    @log_action("add_training_program")
    def add_training_program(class_id, member_username, exercises, coach_username,
                             classes_list, users_dict, programs_dict):
        cls = _get_owned_class(coach_username, class_id, classes_list)
        if cls is None:
            return False, "This class does not exist or does not belong to you."
        if member_username not in users_dict:
            return False, "Member not found."
        if not cls.has_active_member(member_username):
            return False, "This member has no active enrollment in this class."
        if _key(class_id, member_username) in programs_dict:
            return False, "A program already exists for this member; use add/edit exercise."
        if not exercises:
            return False, "A program must have at least one exercise."
        built = []
        for item in exercises:
            ok, msg, ex = CoachService._build_exercise(item)
            if not ok:
                return False, msg
            built.append(ex)
        programs_dict[_key(class_id, member_username)] = TrainingProgram(
            class_id, member_username, coach_username, built)
        return True, "Training program created."

    @staticmethod
    def _owned_program(class_id, member_username, coach_username, classes_list, programs_dict):
        cls = _get_owned_class(coach_username, class_id, classes_list)
        if cls is None:
            return None, "This class does not exist or does not belong to you."
        program = programs_dict.get(_key(class_id, member_username))
        if program is None:
            return None, "There is no program for this member."
        return program, ""

    @staticmethod
    @log_action("add_exercise")
    def add_exercise(class_id, member_username, exercise, coach_username, classes_list, programs_dict):
        program, msg = CoachService._owned_program(class_id, member_username, coach_username,
                                                   classes_list, programs_dict)
        if program is None:
            return False, msg
        ok, msg, ex = CoachService._build_exercise(exercise)
        if not ok:
            return False, msg
        program.add_exercise(ex)
        return True, "Exercise added."

    @staticmethod
    @log_action("edit_exercise")
    def edit_exercise(class_id, member_username, index, new_data, coach_username,
                      classes_list, programs_dict):
        program, msg = CoachService._owned_program(class_id, member_username, coach_username,
                                                   classes_list, programs_dict)
        if program is None:
            return False, msg
        if not isinstance(index, int) or not (0 <= index < len(program.exercises)):
            return False, "Invalid exercise number."
        merged = program.exercises[index].to_dict()
        merged.update({k: v for k, v in new_data.items() if v is not None})
        ok, msg, ex = CoachService._build_exercise(merged)
        if not ok:
            return False, msg
        program.exercises[index] = ex
        return True, "Exercise updated."

    @staticmethod
    def get_program(coach_username, class_id, member_username, classes_list, programs_dict):
        program, msg = CoachService._owned_program(class_id, member_username, coach_username,
                                                   classes_list, programs_dict)
        if program is None:
            return False, msg, None
        return True, "", program
