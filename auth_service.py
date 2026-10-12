class AuthService:

    def login(self ,role , username , password , user_dict ):
        
        account =user_dict.get (username)
        if account is None:
            return False,"invalid username or password", None

        if account.password !=password:
            return False , "invalid username or password" , None

        if role!= account.role:
            return False ,"invalid account type", None

        if  not account.is_active:
            return False , "account is inactive" , None
        return True ,"login successful" , account 
 
        

        
        