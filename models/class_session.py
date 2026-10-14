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

    
    def capacity_remaining(self):
        active_list = self.active_enrollments()   
        taken = len(active_list)               
        remaining = self.capacity - taken         

        if remaining < 0:                         
            remaining = 0

        return remaining
        
    def to_dict(self):
        pass