class User:
    def init(self,name,username,password,email,is_active=True,role="user"):
        self.name=name
        self.username=username
        self.password=password
        self.email=email
        self.is_active=is_active
        self.role=role
        pass

    def to_dict(self):
        return {
            
        }
        pass

class Admin(User):
    pass

class Coach(User):
    pass

class Member(User):
    pass