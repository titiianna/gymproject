class Hall:
    def __init__(self,name,capacity,equipment=None,is_active=True):
        self.name=name
        self.capacity=capacity
        if equipment is None:
            self.equipment = []
        else:
            self.equipment = equipment
        self.is_active=is_active

    def to_dict(self):
        return {
            "name":self.name ,
            "capacity":self.capacity ,
            "equipment":self.equipment ,
            "is_active":self.is_active
        }
    @classmethod
    def from_dict(cls , data):
        return cls (
    
            name = data["name"],
            capacity = data["capacity"],
            equipment = data.get("equipment", None ),
            is_active = data.get("is_active", True)
        )
        
