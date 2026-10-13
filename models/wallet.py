class Transaction:
    def __init__(self,tx_type,amount,date,description,tracking_id):
        self.tx_type=tx_type
        self.amount=amount
        self.date=date
        self.description=description
        self.tracking_id=tracking_id
        
    def to_string_format(self):
        string_format = f"{self.tx_type} | amount = {self.amount} | tx date = {date} | {self.description} | ti = {self.tracking_id} "
        pass

    def to_dict(self):
        return {
            "tx_type":self.tx_type,
            "amount":self.amount,
            "date":self.date,
            "description":self.description,
            "tracking_id":self.tracking_id
        }




class Wallet:
    def __init__(self,username,balance=0.0):
        self.username=username
        self.balance=balance
        pass
    def deposit(amount):
        pass
    def withdraw(amount):
        return True
    