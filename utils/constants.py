from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

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
    return BASE_DIR / "data"

def data_path(filename):
    return BASE_DIR / filename