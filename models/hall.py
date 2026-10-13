class Hall:
    def __init__(self,name,capacity,equipment=None,is_active=True):
        self.name=name
        self.capacity=capacity
        self.equipment=equipment
        self.is_active=is_active

    def to_dict(self):
        return {
            "name":self.name ,
            "capacity":self.capacity ,
            "equipment":self.equipment ,
            "is_active":self.is_active
        }

