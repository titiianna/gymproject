class Validators:

    @staticmethod
    def validate_password(password: str):
        special_sym = ['@', '&']

        if not any(c.isalpha() for c in password):
            return False
        
        if not any(c.isdigit() for c in password):
            return False

        if not any(c in special_sym for c in password):
            return False

        return True

    @staticmethod
    def validate_email():
        pass

    @staticmethod
    def validate_username_unique():
        pass
