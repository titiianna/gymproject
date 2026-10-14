from models.hall import Hall
from utils.validators import Validators


class AdminService:
#بخش افزودن سالن جدید 

    @staticmethod
    def add_hall(name, capacity, equipment, is_active, halls_dict):

#بخش بررسی   نام سالن 
     if not isinstance (name ,str ) :
        return False, "invalid hall name "

     name= name.strip()

#بررسی خالی نبودن نام 
     if not name :
        return False , "hall name cannot be empty "

#بررسی تکراری نبودن نام 
     if name in halls_dict:
        return False , "hall already exists "

#بررسی ظرفیت  سالن 
     if not Validators.positive_int_validate(capacity):
      return False , "invalid hall capacity "

#بخش بررسی تجهیزات سالن 
     if not isinstance(equipment , list ):
        return False , "equipment must be a list "

     if not isinstance (is_active , bool):
        return False , "invalid hall status"
#اماده سازی تجهیزات سالن 
     hall_equipment =[]
     for item in equipment:
        item= str (item).strip()
#اضافه کردن تجهیزات 
        if item:
           hall_equipment.append(item)

       
    


     

     

     