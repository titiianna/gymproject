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
            "name":self.name ,
            "username":self.username,
            "password":self.password,
            "email":self.email,
            "is_active":self.is_active,
            "role":self.role
            }
        
    @classmethod
    def from_dict(cls, data):
        return cls(
            name = data["name"],
            username = data["username"],
            password = data["password"],
            email = data["email"],
            is_active = data.get("is_active", True),
        )



class Admin(User):
    def __init__(self, name, username, password, email, is_active=True):
        return super().__init__(name, username, password, email, is_active, role="admin")
    

class Coach(User):
    def __init__(self, name, username, password, email, is_active=True):
        return super().__init__(name, username, password, email, is_active, role="coach")
    

class Member(User):
    def __init__(self, name, username, password, email, is_active=True,subscription_status="بدون اشتراک", subscription_start=None,
                 subscription_end=None, registered_classes=None,):
        return super().__init__(name, username, password, email, is_active,subscription_status="بدون اشتراک", subscription_start=None,
                 subscription_end=None, registered_classes=None, role="member")
