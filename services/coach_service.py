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
    @staticmethod
    def validate_exercise(exercise):
        """خروجی: (ok, msg). ست/تکرار مثبت و استراحت غیرمنفی."""
        if isinstance(exercise, dict):
            try:
                exercise = Exercise.from_dict(exercise)
            except (TypeError, ValueError, KeyError):
                return False, "اطلاعات حرکت کامل یا معتبر نیست."
    
        required_attrs = ("name", "sets", "reps", "rest_seconds")
        if not all(hasattr(exercise, attr) for attr in required_attrs):
            return False, "ساختار اطلاعات حرکت معتبر نیست."
    
        if not str(exercise.name).strip():
            return False, "نام حرکت نمی‌تواند خالی باشد."
    
        try:
            sets = int(exercise.sets)
            reps = int(exercise.reps)
            rest = int(exercise.rest_seconds)
        except (TypeError, ValueError):
            return False, "ست، تکرار و زمان استراحت باید عدد صحیح باشند."
    
        if sets <= 0:
            return False, "تعداد ست باید بزرگ‌تر از صفر باشد."
        if reps <= 0:
            return False, "تعداد تکرار باید بزرگ‌تر از صفر باشد."
        if rest < 0:
            return False, "زمان استراحت نمی‌تواند منفی باشد."
    
        return True, "حرکت معتبر است."
    
    @staticmethod
    def add_training_program(
        class_id, member_username, exercises, coach_username,
        classes_list, users_dict, programs_dict
    ):
        """برای عضوِ ثبت‌نام‌شده در کلاسِ خود مربی برنامه می‌سازد."""
        class_obj = CoachService._find_class(class_id, classes_list)
        if class_obj is None:
            return False, "کلاس موردنظر پیدا نشد."
    
        if getattr(class_obj, "coach_username", None) != coach_username:
            return False, "فقط برای کلاس‌های خودتان می‌توانید برنامه ثبت کنید."
    
        member = users_dict.get(member_username)
        if member is None or getattr(member, "role", None) != "member":
            return False, "عضو موردنظر پیدا نشد."
        if not getattr(member, "is_active", False):
            return False, "حساب این عضو غیرفعال است."
    
        if not CoachService._is_active_member_of_class(class_obj, member_username, member):
            return False, "این عضو ثبت‌نام فعال در کلاس انتخاب‌شده ندارد."
    
        if not exercises:
            return False, "برنامه باید حداقل یک حرکت داشته باشد."
    
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
            return False, "برای این عضو در این کلاس برنامه وجود دارد؛ از add_exercise استفاده کنید."
    
        programs_dict[key] = TrainingProgram(
            class_id=class_id,
            member_username=member_username,
            coach_username=coach_username,
            exercises=valid_exercises,
        )
        return True, "برنامهٔ تمرینی با موفقیت ثبت شد."
    
    @staticmethod
    def add_exercise(
        class_id, member_username, exercise, coach_username,
        classes_list, programs_dict
    ):
        """یک حرکت به برنامهٔ موجود اضافه می‌کند."""
        class_obj = CoachService._find_class(class_id, classes_list)
        if class_obj is None:
            return False, "کلاس موردنظر پیدا نشد."
        if getattr(class_obj, "coach_username", None) != coach_username:
            return False, "فقط می‌توانید برنامهٔ کلاس‌های خودتان را تغییر دهید."
    
        ok, msg = CoachService.validate_exercise(exercise)
        if not ok:
            return False, msg
        if isinstance(exercise, dict):
            exercise = Exercise.from_dict(exercise)
    
        key = CoachService._program_key(class_id, member_username)
        program = programs_dict.get(key)
        if program is None:
            return False, "برای این عضو هنوز برنامه‌ای ثبت نشده است."
        if getattr(program, "coach_username", None) != coach_username:
            return False, "اجازهٔ تغییر این برنامه را ندارید."
    
        try:
            program.add_exercise(exercise)
        except (TypeError, ValueError) as error:
            return False, f"افزودن حرکت انجام نشد: {error}"
        return True, "حرکت با موفقیت به برنامه اضافه شد."
    
    @staticmethod
    def edit_exercise(
        class_id, member_username, index, new_data, coach_username,
        classes_list, programs_dict
    ):
        """حرکت را با index صفرمبنا ویرایش می‌کند؛ اولین حرکت index=0 است."""
        class_obj = CoachService._find_class(class_id, classes_list)
        if class_obj is None:
            return False, "کلاس موردنظر پیدا نشد."
        if getattr(class_obj, "coach_username", None) != coach_username:
            return False, "فقط می‌توانید برنامهٔ کلاس‌های خودتان را تغییر دهید."
    
        key = CoachService._program_key(class_id, member_username)
        program = programs_dict.get(key)
        if program is None:
            return False, "برنامهٔ تمرینی پیدا نشد."
        if getattr(program, "coach_username", None) != coach_username:
            return False, "اجازهٔ تغییر این برنامه را ندارید."
    
        try:
            index = int(index)
        except (TypeError, ValueError):
            return False, "شمارهٔ حرکت معتبر نیست."
        if index < 0 or index >= len(program.exercises):
            return False, "شمارهٔ حرکت خارج از محدوده است."
    
        if isinstance(new_data, dict):
            try:
                new_exercise = Exercise.from_dict(new_data)
            except (TypeError, ValueError, KeyError):
                return False, "اطلاعات حرکت جدید معتبر نیست."
        elif isinstance(new_data, Exercise):
            new_exercise = new_data
        else:
            return False, "اطلاعات حرکت جدید معتبر نیست."
    
        ok, msg = CoachService.validate_exercise(new_exercise)
        if not ok:
            return False, msg
    
        program.exercises[index] = new_exercise
        return True, "حرکت با موفقیت ویرایش شد."
    
    @staticmethod
    def get_program(
        coach_username, class_id, member_username, classes_list, programs_dict
    ):
        """خروجی: (ok, msg, TrainingProgram | None)."""
        class_obj = CoachService._find_class(class_id, classes_list)
        if class_obj is None:
            return False, "کلاس موردنظر پیدا نشد.", None
        if getattr(class_obj, "coach_username", None) != coach_username:
            return False, "شما اجازهٔ مشاهدهٔ برنامهٔ این کلاس را ندارید.", None
    
        key = CoachService._program_key(class_id, member_username)
        program = programs_dict.get(key)
        if program is None:
            return True, "برای این عضو در این کلاس هنوز برنامه‌ای ثبت نشده است.", None
        if getattr(program, "coach_username", None) != coach_username:
            return False, "شما اجازهٔ مشاهدهٔ این برنامه را ندارید.", None
    
        return True, "برنامهٔ تمرینی دریافت شد.", program
    