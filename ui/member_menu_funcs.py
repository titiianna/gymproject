from database import save_all
from services.admin_service import AdminService
from services.member_service import MemberService as S
from ui.helpers import ask, pick, show_table


def _profile(member, db):
    p = S.get_profile(member.username, db["users"])

    print("Name: " + str(p["name"]))
    print("Username: " + str(p["username"]))
    print("Email: " + str(p["email"]))
    print("Account status: " + str(p["account_status"]))
    print("Plan: " + str(p["subscription_type"]))
    print("Start date: " + str(p["subscription_start"]))
    print("End date: " + str(p["subscription_end"]))
    print("Subscription status: " + str(p["subscription_status"]))


def _programs(member, db):
    programs = S.get_member_programs(member.username, db["programs"], db["classes"])

    if len(programs) == 0:
        print("No training program has been set for you yet.")

    for prog in programs:
        cls = None
        for x in db["classes"]:
            if x.class_id == prog.class_id:
                cls = x
                break

        if cls != None:
            print("\nClass: " + cls.title)
        else:
            print("\nClass: " + prog.class_id)

        rows = []
        for e in prog.exercises:
            rows.append((e.name, e.sets, e.reps, e.rest_seconds, e.description))

        show_table(["Exercise", "Sets", "Reps", "Rest (seconds)", "Description"], rows)


def _view_balance(member, db):
    bal = S.get_balance(member.username, db["wallets"])
    print("Balance: " + format(int(bal), ","))


def _top_up_wallet(member, db):
    amount = ask("Amount")

    card = None
    if amount != None:
        card = ask("Card number (16 digits)")

    month = None
    if card != None:
        month = ask("Expiry month")

    year = None
    if month != None:
        year = ask("Expiry year")

    password = None
    if year != None:
        password = ask("Card password (6 digits)")

    cvv2 = None
    if password != None:
        cvv2 = ask("CVV2")

    if cvv2 == None:
        return

    result = S.deposit_wallet(member.username, amount, card, month, year, password,
                              cvv2, db["wallets"], db["transactions"])
    ok = result[0]
    msg = result[1]

    if ok == True:
        print("✔ " + msg)
    else:
        print("✘ " + msg)

    if ok == True:
        save_all(db)


def _view_transactions(member, db):
    txs = S.list_transactions(member.username, db["transactions"])

    rows = []
    for t in txs:
        rows.append((t.tx_type, format(int(t.amount), ","), t.date, t.description, t.tracking_id))

    show_table(["Type", "Amount", "Date", "Description", "Tracking number"], rows)


def _pay_for_plan(member, db):
    plans = AdminService.list_plans(db["plans"])
    plan = pick("Choose a plan", plans, lambda p: p.title + " - " + format(p.price, ","))

    if plan == None:
        return

    result = S.subscribe(member.username, plan.title, db["plans"], db["wallets"],
                         db["users"], db["payments"], db["transactions"])
    ok = result[0]
    msg = result[1]

    if ok == True:
        print("✔ " + msg)
    else:
        print("✘ " + msg)

    if ok == True:
        save_all(db)


def _show_classes(member, db):
    classes = []
    for x in db["classes"]:
        if x.has_active_member(member.username):
            classes.append(x)

    rows = []
    for c in classes:
        coach = db["users"].get(c.coach_username)

        if coach != None:
            coach_name = coach.name
        else:
            coach_name = c.coach_username

        rows.append((c.title, c.sport_type, coach_name, c.hall_name,
                     c.day, c.time, c.capacity, c.capacity_remaining))

    show_table(["Title", "Sport", "Coach", "Hall", "Day", "Time", "Total capacity", "Remaining"], rows)


def _enroll_class(member, db):
    classes = S.list_available_classes(db["classes"])
    cls = pick("Choose a class", classes,
               lambda x: x.title + " - " + x.day + " " + x.time + " (remaining " + str(x.capacity_remaining) + ")")

    if cls == None:
        return

    result = S.enroll_class(member.username, cls.class_id, db["users"], db["classes"])
    ok = result[0]
    msg = result[1]

    if ok == True:
        print("✔ " + msg)
    else:
        print("✘ " + msg)

    if ok == True:
        save_all(db)


def _cancel_class(member, db):
    mine = []
    for x in db["classes"]:
        if x.has_active_member(member.username):
            mine.append(x)

    cls = pick("Which class do you want to cancel?", mine, lambda x: x.title + " - " + x.day + " " + x.time)

    if cls == None:
        return

    result = S.cancel_class_enrollment(member.username, cls.class_id, db["users"], db["classes"])
    ok = result[0]
    msg = result[1]

    if ok == True:
        print("✔ " + msg)
    else:
        print("✘ " + msg)

    if ok == True:
        save_all(db)