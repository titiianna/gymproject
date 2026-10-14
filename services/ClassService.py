@staticmethod
def _make_class_data(title ,sport_type , coach_username
                      , hall_name , day , time , capacity  ):
#ساخت دیکشنری اطلاعات کلاس 
    return{"title":title , "sport_type" :sport_type , "coach_username" : coach_username ,
           "hall_name" : hall_name , "day":day , "time" :time ,"capacity":capacity}

#اعتبار سنجی زمان کلاس 
@staticmethod
def _check_class_conflict(class_data, classes_list, class_id=None):
#بررسی کلاس های فعال برای پیدا کردم تداخل 
       for current_class in classes_list:
             if current_class.class_id == class_id :
                continue
             if ( current_class.day == class_data["day" ] and 
                  current_class.time == class_data[ "time"] ):
              if ( current_class.coach_username ==class_data[ "coach_username" ] ):
                  return False , "the instructor has another class at this time"
             if current_class.hall_name == class_data [ "hall_name"]:
                 return False , " the hall is reserved at this time"
       return True , ""

#اعتبار سنجی اطلاعا کلاس 
@staticmethod
def _check_class(class_data , users_dict , halls_dict , classes_list , class_id=None):
    title=class_data["title"]
    sport_type=class_data["sport_type"]
    coach_username = class_data ["coach_username"]
    hall_name = class_data ["hall_name"]
    day = class_data ["day"]
    time= class_data ["time"]
    capacity = class_data ["capacity"]
    allowed_sports = {"Bodybuilding", "Yoga", "Pilates"}
#بررسی عنوان کلاس 
    if not isinstance (title , str ) or not title.strip():
        return False , "The class title cannot be empty"
    if sport_type not in allowed_sports :
        return False , "The type of sport is invalid"
    coach= users_dict.get (coach_username )
    if coach is None or coach.role != role_coach:
        return False , "No coach was found"
    if not coach.is_active:
        return False , "The coach is not available"
    hall = halls_dict.get (hall_name)
    if hall is None :
        return False , "The requested hall was not found"
    if not validators.day_validate(day):
        return False , "The scheduled date is incorrect"
    if not validators.time_validate(time):
        return False , "Incorrect scheduled time"
    if not validators.positive_int_validate (capacity):
        return False , "The capacity must be a positive integer"
    capacity = int (capacity)
    if capacity > hall.capacity:
        return False , "The capacity of the classroom is greater than the capacity of the hall"

    ok,msg= AdminService_.check_class_conflict (class_data , classes_list , class_id)
    if not ok:
            return False, msg

    return True, ""

@staticmethod
@log_action("create_class")
def create_class(title , sport_type ,coach_username , hall_name ,
                     day , time , capacity , users_dict , halls_dict ,classes_list ):
#بخش دیکشنری اطلاعات کلاس 
        class_data = AdminService._make_class_data(title , sport_type, 
                                                  coach_username , hall_name , 
                                                  day , time , capacity )

        ok,msg = AdminService._check_class(
            class_data , users_dict
            , halls_dict ,classes_list 

        )

        if not ok:
            return False, msg
#سناسه کلاس 
        class_id = IdGenerator.class_id(classes_list )

        new_class = ClassSession (
            class_id , 
            class_data["title "].strip() , 
            class_data["sport_type"],
            class_data["coach_username"],
            class_data["hall_name"],
            class_data["day"],
            class_data["time"],
            int(class_data["capacity"]),
        )
#اضافه کردن کلاس به فهرست
        classes_list.append(new_class)
        return True , f"Class with id {class_id} Created "

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
    current_class = None

    for item in classes_list:
        if item.class_id == class_id:
            current_class = item
            break

# اگر کلاس پیداجدید وارد نشد قبلی حغظ بشه 
    if current_class is None:
        return False, "Class not found"
    if title is None:
        title = current_class.title
    if sport_type is None:
        sport_type = current_class.sport_type
    if coach_username is None:
        coach_username = current_class.coach_username
    if hall_name is None:
        hall_name = current_class.hall_name
    if day is None:
        day = current_class.day
    if time is None:
        time = current_class.time
    if capacity is None:
        capacity = current_class.capacity
    class_data = AdminService._make_class_data(
        title,
        sport_type,
        coach_username,
        hall_name,
        day,
        time,
        capacity,
    )

# شمارش ثبت‌نام‌های فعال
    active_enrollments = 0

    for enrollment in current_class.enrollments:
     if enrollment.is_active:
        active_enrollments += 1

    if int(class_data["capacity"]) < active_enrollments:
     return False, "The capacity cannot be less than the active registrations."

    ok, message = AdminService._check_class(
        class_data,
        users_dict,
        halls_dict,
        classes_list,
        class_id=class_id,
    )

    if not ok:
        return False, message

    current_class.title = class_data["title"]
    current_class.sport_type = class_data["sport_type"]
    current_class.coach_username = class_data["coach_username"]
    current_class.hall_name = class_data["hall_name"]
    current_class.day = class_data["day"]
    current_class.time = class_data["time"]
    current_class.capacity = int(class_data["capacity"])

    return True, "Class updated successfully"

@staticmethod
@log_action("toggle_class_status")
def toggle_class_status(class_id, classes_list):
    current_class = None
    for item in classes_list:
       if item.class_id == class_id:
        current_class = item
        break
    if current_class is None:
      return False, "Class not found"
    if not current_class.is_active:
        class_data = {
            "coach_username" : current_class.coach_username ,
            "hall_name" : current_class.hall_name ,
            "day" : current_class.day ,
            "time" : current_class.time ,
        }
        ok, msg = AdminService._check_class_conflict(
            class_data ,
            classes_list ,
            class_id,
            )
        if not ok:
            return False, msg

        current_class.is_active = not current_class.is_active
        if current_class.is_active:
            return True, "The class has been activated"
        return True,"The class has been deactivated"
@staticmethod
def list_classes(classes_list):
    return list(classes_list)



   