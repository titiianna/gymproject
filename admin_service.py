import models.user 
import models.wallet 
import utils.validators

class AdminService:
    def add_user (self , role , name , username ,password , email , 
                 is_active , user_dict ,wallets_dict ):
        user_roles = {"coach" , "member"}

        if role not in user_roles:
            return False , "invalid role provided"
    

#بخش اعتبار سنجی اطلاعات کاربر 
        if not isinstance(name ,str ):
            return False , "invalid name provided"
        name = name.strip()

        if not utils.validators.username_validate(username):
            return False , "invalid username provided"
        if not utils.validators.name_validate(name):
            return False , "invalid name provided"
        if username in user_dict:
            return False , "username already exists"
        if not utils.validators.password_validate(password):
            return False , "invalid password provided"
        if not utils.validators.email_validate(email):
            return False , "invalid email provided"
        if not isinstance(is_active , bool):
            return False , "invalid active status provided"

#بخش انتخاب کلاس و ساخت کاربر

        user_classes = {
            "coach" :models.user.Coach , 
            "member" : models.user.Member
        }

        user_class= user_classes[role]
        user= user_class(
            name.strip(), 
            username ,
            password ,
            email ,
            is_active
        )
#ساخت کیف پول و ذخیره کاربر
        if role == "member":
            wallets_dict.setdefault(
                username , models.wallet.Wallet(username)

            )  
        
        user_dict[username]= user
        return True , "user added successfully"
