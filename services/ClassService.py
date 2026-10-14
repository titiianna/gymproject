
@staticmethod
def _make_class_data(title ,sport_type , coach_username
                      , hall_name , day , time , capacity  ):
#ساخت دیکشنری اطلاعات کلاس 
    return{"title":title , "sport_type" :sport_type , "coach_username" : coach_username ,
           "hall_name" : hall_name , "day":day , "time" :time ,"capacity":capacity}

#اعتبار سنجی زمان کلاس 
@staticmethod
def _check_class_conflict(class_data, classes_list, class_id=None):
    for current_class in classes_list:

        if current_class.class_id == class_id:
            continue

        if not current_class.is_active:
            continue

        if (
            current_class.day == class_data["day"]
            and current_class.time == class_data["time"]
        ):
            if current_class.coach_username == class_data["coach_username"]:
                return False, "The instructor has another class at this time"

            if current_class.hall_name == class_data["hall_name"]:
                return False, "The hall is reserved at this time"

    return True, ""

#اعتبار سنجی اطلاعا کلاس 
# اعتبارسنجی اطلاعات کلاس
@staticmethod
def _check_class(
    title,
    sport_type,
    coach_username,
    hall_name,
    day,
    time,
    capacity,
    users_dict,
    halls_dict,
    classes_list,
    exclude_id=None,
    check_coach=True,
    check_hall=True,
    min_capacity=0,
):
    # بررسی عنوان کلاس
    if not isinstance(title, str) or not title.strip():
        return False, "The class title cannot be empty"
    if sport_type not in SPORT_TYPES:
        return False, "The type of sport is invalid"
    
    coach = users_dict.get(coach_username)

    if coach is None or coach.role != ROLE_COACH:
        return False, "No coach was found"

    if check_coach and not coach.is_active:
        return False, "The coach is not active"
    
    hall = halls_dict.get(hall_name)

    if hall is None:
        return False, "The requested hall was not found"

    if check_hall and not hall.is_active:
        return False, "The hall is not active"

    if not Validators.day_validate(day):
        return False, "The scheduled day is incorrect"

    if not Validators.time_validate(time):
        return False, "The scheduled time is incorrect"

    if not Validators.positive_int_validate(capacity):
        return False, "The capacity must be a positive integer"

    capacity = int(capacity)

    if capacity > hall.capacity:
        return False, "The class capacity exceeds the hall capacity"

    if capacity < min_capacity:
        return False, "The capacity cannot be less than active enrollments"

    # بررسی تداخل کلاس‌ها
    class_data = {
        "coach_username": coach_username,
        "hall_name": hall_name,
        "day": day,
        "time": time,
    }

    ok, msg = AdminService._check_class_conflict(
        class_data,
        classes_list,
        exclude_id,
    )

    if not ok:
        return False, msg

    return True, ""

@staticmethod
@log_action("create_class")
def create_class(
    title,
    sport_type,
    coach_username,
    hall_name,
    day,
    time,
    capacity,
    users_dict,
    halls_dict,
    classes_list,
):
    # اعتبارسنجی اطلاعات کلاس
    ok, msg = AdminService._check_class(
        title,
        sport_type,
        coach_username,
        hall_name,
        day,
        time,
        capacity,
        users_dict,
        halls_dict,
        classes_list,
    )

    if not ok:
        return False, msg

    # تولید شناسه کلاس
    class_id = IdGenerator.class_id(classes_list)

    # ساخت شیء کلاس
    new_class = ClassSession(
        class_id,
        title.strip(),
        sport_type,
        coach_username,
        hall_name,
        day,
        time,
        int(capacity),
    )

    # اضافه کردن کلاس به فهرست
    classes_list.append(new_class)

    return True, f"Class with id {class_id} created"

# بخش ویرایش کلاس
@staticmethod
@log_action("edit_class")
def edit_class(
    class_id,
    title,
    sport_type,
    coach_username,
    hall_name,
    day,
    time,
    capacity,
    users_dict,
    halls_dict,
    classes_list,
):
    # پیدا کردن کلاس
    current_class = next(
        (
            item
            for item in classes_list
            if item.class_id == class_id
        ),
        None,
    )

    if current_class is None:
        return False, "Class not found"

    check_coach = (
        coach_username is not None
        and coach_username != current_class.coach_username
    )

    check_hall = (
        hall_name is not None
        and hall_name != current_class.hall_name
    )


    title = current_class.title if title is None else title
    sport_type = (
        current_class.sport_type
        if sport_type is None
        else sport_type
    )
    coach_username = (
        current_class.coach_username
        if coach_username is None
        else coach_username
    )
    hall_name = (
        current_class.hall_name
        if hall_name is None
        else hall_name
    )
    day = current_class.day if day is None else day
    time = current_class.time if time is None else time
    capacity = (
        current_class.capacity
        if capacity is None
        else capacity
    )

    # شمارش ثبت‌نام‌های فعال
    active_enrollments = sum(
        1
        for enrollment in current_class.enrollments
        if enrollment.is_active
    )

    # اعتبارسنجی اطلاعات کلاس
    ok, msg = AdminService._check_class(
        title,
        sport_type,
        coach_username,
        hall_name,
        day,
        time,
        capacity,
        users_dict,
        halls_dict,
        classes_list,
        exclude_id=class_id,
        min_capacity=active_enrollments,
    )

    if not ok:
        return False, msg

    current_class.title = title.strip()
    current_class.sport_type = sport_type
    current_class.coach_username = coach_username
    current_class.hall_name = hall_name
    current_class.day = day
    current_class.time = time
    current_class.capacity = int(capacity)

    return True, "Class updated successfully"

# فعال یا غیرفعال کردن کلاس
@staticmethod
@log_action("toggle_class_status")
def toggle_class_status(class_id, classes_list):
    # پیدا کردن کلاس
    current_class = next(
        (
            item
            for item in classes_list
            if item.class_id == class_id
        ),
        None,
    )

    if current_class is None:
        return False, "Class not found"

    # هنگام فعال‌سازی، تداخل زمانی بررسی شود
    if not current_class.is_active:
        class_data = {
            "coach_username": current_class.coach_username,
            "hall_name": current_class.hall_name,
            "day": current_class.day,
            "time": current_class.time,
        }

        ok, msg = AdminService._check_class_conflict(
            class_data,
            classes_list,
            class_id,
        )

        if not ok:
            return False, msg

        current_class.is_active = True
        return True, "The class has been activated"

    # غیرفعال کردن کلاس
    current_class.is_active = False
    return True, "The class has been deactivated"
@staticmethod
def list_classes(classes_list):
    return list(classes_list)
