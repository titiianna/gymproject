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
#test change
        

   