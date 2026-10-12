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
    def username_validate(username: str):

        if not isinstance(username, str):
            return False

        pattern = r"^[a-zA-Z0-9_]{3,20}$"

        return bool(re.match(pattern, username))

    @staticmethod
    def unique_username_validate(username: str, users_existing: list | dict):

        return username not in users_existing

    @staticmethod
    def name_validate(name: str):

        if not isinstance(name, str):
            return False

        pattern = r"^[a-zA-Z\u0621-\u06CC]+(?: [u200c\ ]+[a-zA-Z\u0621-\u06CC])*"

        return bool(re.match(pattern, name))

    
        
