import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

ROLE_ADMIN = "admin"
ROLE_COACH = "coach"
ROLE_MEMBER = "member"

SUB_ACTIVE = "Active"
SUB_EXPIRED = "Expired"
SUB_NONE = "No subscription"

TX_DEPOSIT = "deposit"
TX_SUBSCRIPTION = "subscription_payment"

DAYS = ["Saturday", "Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
SPORT_TYPES = ["Bodybuilding", "Yoga", "Fitness", "CrossFit", "Football"]

DAYS_PER_MONTH = 30

def data_dir():
    return os.path.join(BASE_DIR, "data")

def data_path(filename):
    return os.path.join(data_dir(), filename)