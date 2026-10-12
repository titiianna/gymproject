class AuthService:

    def login(self , username , password , user_dict , account_type ):
        
        account =user_dict.get (username)
        if account is None:
            return False,"invalid username or password", None

        if account.password !=password:
            return False , "invalid username or password" , None

        if account_type!= account.account_type:
            return False ,"invalid account type", None

        if  not account.is_active:
            return False , "account is inactive" , None
        return True ,"login successful" , account 
 
        

        
        