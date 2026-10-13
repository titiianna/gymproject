import models.user 
import models.wallet 
import utils.validators

class AdminService:
     @staticmethod
     def add_user ( role , name , username ,password , email , 
                 is_active , users_dict ,wallets_dict ):
        user_roles = {"coach" , "member"}

        if role not in user_roles:
            return False , "invalid role provided"
    

#بخش اعتبار سنجی اطلاعات کاربر 
        if not isinstance(name ,str ):
            return False , "invalid name provided"
        name = name.strip()

        if not utils.validators.Validators.name_validate(name):
                    return False , "invalid name provided"
        if not utils.validators.Validators.username_validate(username):
            return False , "invalid username provided"
        if username in users_dict:
            return False , "username already exists"
        if not utils.validators.Validators.password_validate(password):
            return False , "invalid password provided"
        if not utils.validators.Validators.email_validate(email):
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
            name ,
            username ,
            password ,
            email ,
            is_active
        )
#ساخت کیف پول و ذخیره کاربر
        if role == "member" and username not in wallets_dict:
             wallets_dict[username] = models.wallet.Wallet(username)
        users_dict[username]= user
        return True , "user added successfully"
