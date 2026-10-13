import models.hall

#بخش مدیریت سالن 

@staticmethod 
def add_hall(name , capacity , equipment , is_active , halls_dict ):
   

#بخش اعتبار سنجی سالن 
   if not isinstance (name , str ) or not name.strip():
      return False , "invalid hall name"
   name= name.strip()

   if name in halls_dict:
      return False , "hall name already exists"
   
#بخش اعتبار سنجی ظرفیت سالن  
   if not utils.validators.validators.positive_int_validator(capacity):
      return False , "invalid hall capacity"

#بخش اعتبار سنجی تجهیزات سالن 
   if not isinstance(equipment , list):
      return False , "invalid equipment provided "
#بخش وضعیت سالن 
   if not isinstance(is_active , bool ):
      return False , "invalid active status provided"

#بخش ساخت 
   hall= models.hall.Hall(name , capacity , equipment , is_active)

#ذخیره سالن 
   halls_dict[name]=hall
   return True, "hall added successfuiy"

   @staticmethod
   def edit_hall (old_name , new_name , capacity , equipment , 
                  halls_dict , classes_list):
      
 


   