class Transaction:
    def __init__(self,tx_type,amount,date,description,tracking_id):
        self.tx_type=tx_type
        self.amount=amount
        self.date=date
        self.description=description
        self.tracking_id=tracking_id
        
    def to_string_format(self):
        return f"{self.tx_type} | amount = {self.amount} | date = {self.date} | {self.description} | id = {self.tracking_id}\n"
        

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
        
    def deposit(self , amount):
        if amount<= 0:
            return False
        else:
            self.balance +=amount
            return True


        
    def withdraw(self , amount):
        if amount>self.balance or amount<=0:
            return False
        else:
            self.balance -= amount
            return True

    def to_dict(self):
        return{
            "username":self.username,
            "balance":self.balance
        }