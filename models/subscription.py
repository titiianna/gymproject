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

class Payment:
    def __init__(self, member_username, plan_title, amount, payment_date, start_date, end_date, tracking_id):
        self.member_username=member_username
        self.plan_title=plan_title
        self.amount=amount
        self.payment_date=payment_date
        self.start_date=start_date
        self.end_date=end_date
        self.tracking_id=tracking_id

    def to_dict(self):
        return {
            "member_username":self.member_username,
            "plan_title":self.plan_title,
            "amount":self.amount,
            "payment_date":self.payment_date,
            "start_date":self.start_date,
            "end_date":self.end_date,
            "tracking_id":self.tracking_id
        }
    @classmethod
    def from_dict(cls , data):
        return cls (
            member_username = data["member_username"],
            plan_title = data["plan_title"],
            amount = data["amount"],
            payment = data["payment"],
            start_date = data["start_date"],
            end_date = data["end_date"],
            tracking_id = data["tracking_id"]
        )
          