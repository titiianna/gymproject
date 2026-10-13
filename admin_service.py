import models .user 
import models .wallet 
import utils .validators

class AdminService:
    def add_user(self , role , name , username ,password , email , 
                 is_active , user_dict wallet_dict ):
        user_roles = {"coach" , "member"}

        if role not in user_roles:
            return False , "invalid role provided"
    

#بخش اعتبار سنجی اطلاعات کاربر 

        if not utils.validators.validate_username(username):
            return False , "invalid username provided"
        if not utils.validators.validate_name(name):
            return False , "invalid name provided"
        if username in user_dict:
            return False , "username alredy exists"
        if not utils.validators.validate_password(password):
            return False , "invalid password provided"
        if not utils.validators.validate_email(email):
            return False , "invalid email provided"
        if not isinstance(is_active , bool):
            return False , "invalid active status provided"
        
        
        
        
        


        
