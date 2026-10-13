import model .user 
import models .wallet 
import utils .validators

class AdminService:
    def add_user(self , role , name , username ,password , email , 
                 is_active , user_dict wallet_dict ):
        user_roles = {"coach" , "member"}

        if role not in user_roles:
            return False , "invalid role provided"
        


        
