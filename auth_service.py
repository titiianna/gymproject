class AuthService:

    def login(self , username , password , user_dict ):
        
        account =user_dict.get (username)
        if account is None:
            return False,"Invalid username or password", None