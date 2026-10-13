from models.class_session import ClassSession
from models.hall import Hall
from models.subscription import Payment, SubscriptionPlan
from models.training_program import TrainingProgram
from models.user import Admin, Coach, Member, user_from_dict
from models.wallet import Transaction, Wallet
from utils.constants import ROLE_MEMBER, data_dir, data_path
from utils.file_handler import FileHandler


def seed_data():
    users = {
        "admin": Admin("Pooria Kiani", "admin", "123", "admin@gym.com"),
        "coach1": Coach("Tania Jeddi", "coach1", "123", "coach1@gym.com"),
        "coach2": Coach("Arshia Alirezaei", "coach2", "123", "coach2@gym.com"),
        "member1": Member("Tina Ahmadi", "member1", "123", "member1@gym.com"),
        "member2": Member("Mohammadhossein Taghipoor", "member2", "123", "member2@gym.com"),
        "member3": Member("Ali Gholami", "member3", "123", "member3@gym.com", False),
    }
    halls = {
        "Bodybuilding Hall": Hall("Bodybuilding Hall", 20, ["Treadmill", "Dumbbell", "Bike"]),
        "Football Hall": Hall("Football Hall", 40, ["Ball", "Goal", "Grass"]),
    }
    classes = [
        ClassSession("C001", "Morning Bodybuilding", "Bodybuilding", "coach1", "Bodybuilding Hall", "Saturday", "08:00", 10),
        ClassSession("C002", "Night Football", "Football", "coach2", "Football Hall", "Monday", "20:00", 22),
    ]
    plans = {
        "1-Month": SubscriptionPlan("1-Month", 1, 500000),
        "3-Month": SubscriptionPlan("3-Month", 3, 1300000),
        "6-Month": SubscriptionPlan("6-Month", 6, 2400000),
    }
    wallets = {
        "member1": Wallet("member1",400000.0),
        "member2": Wallet("member2",120000.0),
        "member3": Wallet("member3",230000.0),
    }
    return {"users": users, "halls": halls, "classes": classes, "wallets": wallets,
            "plans": plans, "payments": [], "programs": {}, "transactions": []}


def _load_list(filename, builder):
    raw = FileHandler.load_from_json(data_path(filename))
    if not isinstance(raw, list):
        return []
    items = []
    for record in raw:
        try:
            items.append(builder(record))
        except:
            print(f"Warning: error in {filename} record.")
    return items


def database_init():
    FileHandler.ensure_data_dir(data_dir())
    if FileHandler.load_from_json(data_path("users.json")) is None:
        db = seed_data()
        save_all(db)
        return db

    loaded_users = {}
    for user in _load_list("users.json", user_from_dict):
        loaded_users[user.username] = user

    loaded_wallets = {}
    for wallet in _load_list("wallets.json", Wallet.from_dict):
        loaded_wallets[wallet.username] = wallet

    for user in loaded_users.values():
        if user.role == ROLE_MEMBER:
            if user.username not in loaded_wallets:
                loaded_wallets[user.username] = Wallet(user.username)

    loaded_halls = {}
    for hall in _load_list("halls.json", Hall.from_dict):
        loaded_halls[hall.name] = hall

    loaded_classes = _load_list("classes.json", ClassSession.from_dict)

    loaded_plans = {}
    for plan in _load_list("plans.json", SubscriptionPlan.from_dict):
        loaded_plans[plan.title] = plan

    loaded_payments = _load_list("payments.json", Payment.from_dict)

    loaded_programs = {}
    for program in _load_list("programs.json", TrainingProgram.from_dict):
        key = f"{program.class_id}:{program.member_username}"
        loaded_programs[key] = program

    loaded_transactions = []
    for line in FileHandler.txt_read(data_path("transactions.txt")):
        if line.strip():
            transaction = Transaction.from_string(line)
            if transaction is not None:
                loaded_transactions.append(transaction)

    return {
        "users": loaded_users,
        "wallets": loaded_wallets,
        "halls": loaded_halls,
        "classes": loaded_classes,
        "plans": loaded_plans,
        "payments": loaded_payments,
        "programs": loaded_programs,
        "transactions": loaded_transactions,
    }

def save_all(db):
    ok = True

    users = []
    for user in db["users"].values():
        users.append(user.to_dict())
    ok &= FileHandler.save_to_json(data_path("users.json"), users)

    halls = []
    for hall in db["halls"].values():
        halls.append(hall.to_dict())
    ok &= FileHandler.save_to_json(data_path("halls.json"), halls)

    classes = []
    for class_session in db["classes"]:
        classes.append(class_session.to_dict())
    ok &= FileHandler.save_to_json(data_path("classes.json"), classes)

    wallets = []
    for wallet in db["wallets"].values():
        wallets.append(wallet.to_dict())
    ok &= FileHandler.save_to_json(data_path("wallets.json"), wallets)

    plans = []
    for plan in db["plans"].values():
        plans.append(plan.to_dict())
    ok &= FileHandler.save_to_json(data_path("plans.json"), plans)

    payments = []
    for payment in db["payments"]:
        payments.append(payment.to_dict())
    ok &= FileHandler.save_to_json(data_path("payments.json"), payments)

    programs = []
    for program in db["programs"].values():
        programs.append(program.to_dict())
    ok &= FileHandler.save_to_json(data_path("programs.json"), programs)

    transactions_text = ""
    for transaction in db["transactions"]:
        transactions_text += transaction.format_string() + "\n"

    ok &= FileHandler.txt_write(
        data_path("transactions.txt"),
        transactions_text
    )

    return bool(ok)