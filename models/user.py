class User:
    def init(self,name,username,password,email,is_active=True,role="user"):
        pass

    def to_dict(self):
        pass

class Admin(User):
    pass

class Coach(User):
    pass

class Member(User):
    pass