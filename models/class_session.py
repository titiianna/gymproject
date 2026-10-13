class ClassSession:
    def __init__(self,title,sport_type,coach_username,hall_name,day,time,capacity,is_active=True):
        self.title=title
        self.sport_type=sport_type
        self.coach_username=coach_username
        self.hall_name=hall_name
        self.day=day
        self.time=time
        self.capacity=capacity
        self.is_active=is_active
    
    def remaining_capacity(self):
        
        pass
    def to_dict(self):
        pass