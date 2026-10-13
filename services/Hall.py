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
     

     

     