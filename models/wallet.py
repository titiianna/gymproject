def _fmt_amount(amount):
    if float(amount).is_integer():
        return str(int(amount))
    return str(amount)

def _is_number(x):
    return isinstance(x, (int, float)) and not isinstance(x, bool)

class Transaction:
    def __init__(self, username, tx_type, amount, description, date, tracking_id):
        self.username=username
        self.tx_type=tx_type
        self.amount=amount
        self.description=description
        self.date=date
        self.tracking_id=tracking_id
        
    def format_string(self):
        return f"{self.tracking_id} | {self.username} | {self.tx_type} | {self.amount} | {self.date} | {self.description}\n"
        
    @classmethod
    def from_string(cls,line):
        line_list = line.split("|")
        return cls (
            tracking_id = line_list[0],
            username = line_list[1],
            tx_type = line_list[2],
            amount = line_list[3],
            date = line_list[4],
            description = line_list[5]
        )

        
        
class Wallet:
    def __init__(self,username,balance=0.0):
        self.username=username
        self.balance=balance
        
    def deposit(self , amount):
        if not _is_number(amount) or amount <= 0:
            return False
        else:
            self.balance +=amount
            return True


        
    def withdraw(self , amount):
        if not _is_number(amount) or amount <= 0 or amount > self.balance:
            return False
        else:
            self.balance -= amount
            return True

    def to_dict(self):
        return{
            "username":self.username,
            "balance":self.balance
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
        username=data["username"],
        balance=data.get("balance", 0.0)
    )