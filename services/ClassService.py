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
             
              