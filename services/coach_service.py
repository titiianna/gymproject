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
        
    @staticmethod
    def get_coach_classes(coach_username, classes_list):
        """فهرست کلاس‌های مربی را برمی‌گرداند."""
        return [
            class_obj for class_obj in classes_list
            if getattr(class_obj, "coach_username", None) == coach_username
            ]
    
    @staticmethod
    def get_class_members(coach_username, class_id, classes_list, users_dict):
        """خروجی: (ok, msg, list_of_members)، فقط اعضای ثبت‌نام‌شده فعال."""
        class_obj = CoachService._find_class(class_id, classes_list)
        if class_obj is None:
            return False, "کلاس موردنظر پیدا نشد.", []
    
        if getattr(class_obj, "coach_username", None) != coach_username:
            return False, "شما اجازهٔ دسترسی به اعضای این کلاس را ندارید.", []
    
        members = []
        for username, user in users_dict.items():
            if getattr(user, "role", None) != "member":
                continue
            if not getattr(user, "is_active", False):
                continue
            if CoachService._is_active_member_of_class(class_obj, username, user):
                members.append(user)
    
            return True, "اعضای ثبت‌نام‌شدهٔ فعال دریافت شدند.", members
    