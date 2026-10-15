from datetime import date, timedelta
from utils.constants import DAYS_PER_MONTH, ROLE_ADMIN, ROLE_COACH, ROLE_MEMBER, SUB_ACTIVE, SUB_EXPIRED, SUB_NONE


class User:
    def __init__(self,name,username,password,email,is_active=True,role="user"):
        self.name=name
        self.username=username
        self.password=password
        self.email=email
        self.is_active=is_active
        self.role=role
        

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
        super().__init__(name, username, password, email, is_active, role="admin")
    

class Coach(User):
    def __init__(self, name, username, password, email, is_active=True):
        super().__init__(name, username, password, email, is_active, role="coach")
    

class Member(User):
    def __init__(self, name, username, password, email, is_active=True,subscription_status="بدون اشتراک",subscription_type=None, subscription_start=None,
                 subscription_end=None, registered_classes=None,):
        super().__init__(name, username, password, email, is_active, role="member")
        self.subscription_status = subscription_status
        self.subscription_type = subscription_type
        self.subscription_start = subscription_start
        self.subscription_end = subscription_end
        self.registered_classes = ( [] if registered_classes is None else registered_classes )



    def to_dict(self):
        data = super().to_dict()
        data.update({
            "subscription_status": self.subscription_status,
            "subscription_type": self.subscription_type,
            "subscription_start": self.subscription_start,
            "subscription_end": self.subscription_end,
            "registered_classes": self.registered_classes,
        })
        return data

    @classmethod
    def from_dict(cls, data):
        return cls(
            name=data["name"],
            username=data["username"],
            password=data["password"],
            email=data["email"],
            is_active=data.get("is_active", True),
            subscription_status=data.get("subscription_status", "بدون اشتراک"),
            subscription_start=data.get("subscription_start"),
            subscription_end=data.get("subscription_end"),
            registered_classes=data.get("registered_classes"),
        )

    def refresh_subscription_status(self, today=None):
    
        if today is None:
            today = date.today()
        if self.subscription_end is None:
            self.subscription_status = SUB_NONE
        elif today <= date.fromisoformat(self.subscription_end):
            self.subscription_status = SUB_ACTIVE
        else:
            self.subscription_status = SUB_EXPIRED

        return self.subscription_status
       
    def has_active_subscription(self):
        status = self.refresh_subscription_status() 
        return status == SUB_ACTIVE                  
        

    def activate_subscription(self, plan_title, duration_months, today=None):
        if today is None:
            today = date.today()

        if self.refresh_subscription_status(today) == SUB_ACTIVE:
            start = date.fromisoformat(self.subscription_end)
        else:
            start = today

        end = start + timedelta(days=duration_months * DAYS_PER_MONTH)

        self.subscription_start = start.isoformat()
        self.subscription_end = end.isoformat()
        self.subscription_status = SUB_ACTIVE

        return self.subscription_start, self.subscription_end

        