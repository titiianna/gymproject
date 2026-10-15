class Enrollment:
    def __init__(self, username, date, tracking_id, is_active=True):
        self.username=username
        self.date=date
        self.tracking_id=tracking_id
        self.is_active=is_active

    def cancel(self):
        self.is_active = False

    def to_dict(self):
        return {
            "username":self.username,
            "date":self.date,
            "tracking_id":self.tracking_id,
            "is_active":self.is_active
        }
    @classmethod
    def from_dict(cls , data):
        return cls (
            username = data["username"],
            date = data["date"],
            tracking_id = data["tracking_id"],
            is_active = data.get("is_active", True)
        )