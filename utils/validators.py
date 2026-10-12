import re

class Validators:

    @staticmethod
    def validate_password(password: str):

        if not isinstance(password, str):
            return False
        
        if len(password) < 3 :
            return False
        
        pattern = r"^(?=.*[a-zA-Z])(?=.*\d)(?=.*[@&]).+$"

        return bool(re.match(pattern, password))

    @staticmethod
    def validate_email(email: str):

        if not isinstance(email, str):
            return False
        
        pattern = r"^[^@\s]+@[^@\s]+\.[^@\s]+$"

        return bool(re.match(pattern, email))

    
    @staticmethod
    def validate_username_unique():
        pass
