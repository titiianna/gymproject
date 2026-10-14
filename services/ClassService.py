@staticmethod
def _make_class_data(title ,sport_type , coach_username
                      , hall_name , day , time , capacity  ):
#ساخت دیکشنری اطلاعات کلاس 
    return{"titel":title , "sport_type" :sport_type , "coach_username" : coach_username ,
           "hall_name" : hall_name , "day":day , "time" :time ,"capacity":capacity}

#اعتبار سنجی زمان کلاس 
@staticmethod
def _check_class(class_data, classes_list, class_id=None):
#بررسی کلاس های فعال برای پیدا کردم تداخل 
       for current_class in classes_list:
             if current_class.class_id == class_id :
                continue
#بخش تداخل روز و ساعت 
             if ( current_class.day == class_data[ "day" ] and 
                  current_class.time == class_data[ "time"] ):
#بخش تداخل مربی 
              if ( current_class.coach_username ==class_data[ "coach_username" ] ):
                  return False , "the instructor has another class at this time"
#بخش تداخل سالن 
             if current_class.hall_name == class_data [ "hall_name"]:
                 return False , " the hall is reserved at this time"
       return True , ""

#اعتبار سنجی اطلاعا کلاس 
@staticmethod
def _check_class(class_data , users_dict , halls_dict , alasses_list , class_id=None):
    title=class_data["title"]
    sport_tyoe=class_data[ "sport_type "]
    coach_username = class_data [ "coach_username "]
    hall_name = class_data [ " hall_name "]
    day = class_data [" day"]
    time= class_data [" time "]
    capacity = class_data [" capacity "]
#بررسی عنوان کلاس 
    if not isinstance (title , str ) or not title.strip():
        return False , "The class title cannot be empty"
#بررسی نوغ ورزشی 
    if sport_tyoe not in sport_tyoe :
        return False , "The type of sport is invalid"
    coach= users_dict.get (coach_username )
    if coach is None or coach.role != role_coach:
        return False , "No coach was found"
#بررسی فعال بودن مربی 
    if not coach.is_active:
        return False , "The coach is not available"
#پیدا کردن سالن مورد نظر 
    hall = halls_dict.get (hall_name)
    if hall is None :
        return False , "The requested hall was not found"
#روز برگزاری
    if not validators.day_validate(day):
        return False , "The scheduled date is incorrect"
#بررسی ساعت برگزاری 
    if not valiValidators.time_validate(time):
        return False , "Incorrect scheduled time"
#بخش بررسی ظرفیت 
    if not validators.positive_int_validate (capacity):
        return False , "The capacity must be a positive integer"
    capacity = int (capacity)
#بررسی ظرفیت گلاس . سالن
    if capacity > hall.capacity:
        return False , "The capacity of the classroom is greater than the capacity of the hall"

    ok,msg= AdminService.check_class_conflict (class_data , classes_list , class_id)
    if not ok:
            return False, msg

    return True, ""

    @staticmethod
    @log_action("create_class")
    def create_class(title , sport_type ,coach_username , hall_name ,
                     day , time , capacity , users_dict , halls_dict ,classes_list ):
#بخش دیکشنری اطلاعات کلاس 
        class_data = AdminService_make_class_data(title , sport_tyoe, 
                                                  coach_username , hall_name , 
                                                  day , time , capacity )

        od,msg = AdminService_check_class(
            class_data , users_dict
            , halls_dict ,classes_list 

        )

        if not ok:
            return False, msg
#سناسه کلاس 
        class_id = IdGenerator.class_id(classes_list )

        new_class = ClassSession (
            class_id , 
            class_data[ "title "].strip() , 
            class_data  ["sport_type "]
            class_data["coach_username"],
            class_data["hall_name"],
            class_data["day"]
            class_data["time"]
            int(class_data["capacity"])
        )
#اضافه کردن کلاس به فهرست
        classes_list.append(new_class)
        return True , f"Class with id {class_id} Created "
    




    

    

    
    
    



    
    
    
