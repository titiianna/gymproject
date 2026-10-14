from models.hall import Hall
from utils.validators import Validators


class AdminService:
    # بخش افزودن سالن جدید
    @staticmethod
    def add_hall(name, capacity, equipment, is_active, halls_dict):
        # بررسی نام سالن
        if not isinstance(name, str):
            return False, "invalid hall name"

        name = name.strip()

        # بررسی خالی نبودن نام
        if not name:
            return False, "hall name cannot be empty"

        # بررسی تکراری نبودن نام
        if name in halls_dict:
            return False, "hall already exists"

        # بررسی ظرفیت سالن
        if not Validators.positive_int_validate(capacity):
            return False, "invalid hall capacity"

        # بررسی تجهیزات سالن
        if not isinstance(equipment, list):
            return False, "equipment must be a list"

        if not isinstance(is_active, bool):
            return False, "invalid hall status"

        # آماده‌سازی تجهیزات سالن
        hall_equipment = []
        for item in equipment:
            cleaned_item = str(item).strip()
            if cleaned_item:
                hall_equipment.append(cleaned_item)

        hall = Hall(name=name, capacity=capacity, equipment=hall_equipment, is_active=is_active)

        # ذخیره سالن در دیکشنری
        halls_dict[name] = hall
        return True, "hall added successfully"
#بخش ویرایش اطلاعات سالن 
    @staticmethod
    def edit_hall(old_name , new_name , capacity , equipment , halls_dict ,classes_list ):
        hall =halls_dict.get(old_name)

        if hall is None:
            return False , "hall not found "

        def validate_name (value):
            if not isinstance(value, str ):
                return False 

            value= value.strip()
#نام نباید خالی باشه
            if not value:
                return False
#نام نباید متعلق به سالن دیگر باشد 
            if value != old_name and value in halls_dict:
                return False 
            return True
#اعتبار سنجحی نام جدید 
        if new_name is not None :
            if not validate_name( new_name ):
                return False , "invalid or duplicate hall name "
            new_name= new_name.strip()
#اعتبار سنجی ظرفیت جدید 
        if capacity is not None:
            if not Validators.positive_int_validate(capacity):
                return False , "invalid capacity "

            related_classes=[]

            for session in classes_list:
                if session.hall_name == old_name:
                    related_classes.append(session)
#ظرفیت سالن نباید کمتر باشه از کلاسای مرتبطش 
                    for session in related_classes:
                        if session.capacity > capacity:
                            return False ," new capacity is too small"
#بخش بررسی تجهیزات جدید 
                        if equipment is not None :
                            if not isinstance (equipment , list):
                                return False , "equipment must be a list"
#اعمال ظرفیت جدید 
                        if capacity is not None :
                            hall.capacity= capacity

                        if equipment is not None :
                            hall.equipment = [
                                 str(item ).strip()
                                 for item in equipment
                                 if str(item ).strip()
                            ]
                            


                        





            
            


            

            
     

     