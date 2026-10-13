import models.hall

#بخش مدیریت سالن 

@staticmethod 
def hall(name , capacity , equipment , is_active , halls_dict ):
   

#بخش اعتبار سنجی سالن 
   if not isinstance (name , str ) or not name.strip():
      return False , "invalid hall name"
