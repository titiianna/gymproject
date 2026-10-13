class SubscriptionPlan:
    def __init__(self,title,duration_months,price):
        self.title=title
        self.duration_months=duration_months
        self.price=price 

    def to_dict(self):
        return {
            "title":self.title,
            "duration_months":self.duration_months,
            "price":self.price
        }
    @classmethod
    def from_dict(cls , data):
        return cls (
            title = data["title"],
            duration_months = data["duration_months"],
            price = data["price"]
        )