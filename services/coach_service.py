from models.training_program import Exercise, TrainingProgram


class CoachService:
    """منطق پنل مربی؛ مربی فقط به کلاس‌ها و اعضای خودش دسترسی دارد."""

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