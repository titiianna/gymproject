from models.enrollment import Enrollment

class ClassSession:
    def __init__(self,class_id,title,sport_type,coach_username,hall_name,day,time,capacity,is_active=True,enrollments=None):
        self.class_id=class_id
        self.title=title
        self.sport_type=sport_type
        self.coach_username=coach_username
        self.hall_name=hall_name
        self.day=day
        self.time=time
        self.capacity=capacity
        self.is_active=is_active
        self.enrollments=[] if enrollments is None else enrollments

    def active_enrollments(self):
        result = []
        for e in self.enrollments:
            if e.is_active:
                result.append(e)
        return result

    @property
    def capacity_remaining(self):
        active_list = self.active_enrollments()   
        taken = len(active_list)               
        remaining = self.capacity - taken         

        if remaining < 0:                         
            remaining = 0

        return remaining

    @property
    def is_full(self):
        return self.capacity_remaining <= 0

    def get_enrollment(self, username):
        for e in self.active_enrollments():
            if e.username == username:
                return e
        return None

    def has_active_member(self, username):
        return self.get_enrollment(username) is not None

    def active_member_usernames(self):
        result = []                                  
        for e in self.active_enrollments():           
            result.append(e.username)                 
        return result

    def to_dict(self):
        return {
            "class_id":self.class_id,
            "title":self.title,
            "sport_type":self.sport_type,
            "coach_username":self.coach_username,
            "hall_name":self.hall_name,
            "day":self.day,
            "time":self.time,
            "capacity":self.capacity,
            "is_active":self.is_active,
            "enrollments":[e.to_dict() for e in self.enrollments],
        }
        
    @classmethod
    def from_dict(cls, data):
        enrollments = [Enrollment.from_dict(e) for e in data.get("enrollments", [])]
        return cls(
            class_id=data["class_id"],
            title=data["title"],
            sport_type=data["sport_type"],
            coach_username=data["coach_username"],
            hall_name=data["hall_name"],
            day=data["day"],
            time=data["time"],
            capacity=data["capacity"],
            is_active=data.get("is_active", True),
            enrollments=enrollments,
        )
 