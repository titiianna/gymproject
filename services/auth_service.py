class AuthService:
    @staticmethod
    def login(role, username, password, users_dict):
        user = users_dict.get(username)
        if user is None or user.role != role or user.password != password:
            return False, "Incorrect username or password.", None
        if not user.is_active:
            return False, "This account is inactive.", None
        return True, "Login successful.", user