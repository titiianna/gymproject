from database import save_all
from services.admin_service import AdminService as S
from utils.constants import DAYS, ROLE_COACH, ROLE_MEMBER, SPORT_TYPES, data_path
from utils.file_handler import FileHandler
from ui.helpers import ask, ask_active, ask_choice, menu, opt, pick, show_table


def _done(result, db):
    ok = result[0]
    msg = result[1]
    if ok == True:
        print("✔ " + msg)
    else:
        print("✘ " + msg)
    if ok == True:
        save_all(db)


def _add_user(db):
    kind = ask_choice("User type", ["Coach", "Member"])
    if kind == None:
        return
    name = ask("Name")
    username = None
    if name != None:
        username = ask("Username")
    password = None
    if username != None:
        password = ask("Password")
    email = None
    if password != None:
        email = ask("Email")
    active = None
    if email != None:
        active = ask_active("Account status")
    if active == None:
        return

    if kind == "Coach":
        role = ROLE_COACH
    else:
        role = ROLE_MEMBER

    result = S.add_user(role, name, username, password, email, active, db["users"], db["wallets"])
    _done(result, db)


def _edit_user(db):
    username = ask("Username to edit")
    if username == None:
        return
    if username not in db["users"]:
        print("✘ User not found.")
        return
    print("Press Enter to leave a field unchanged.")
    name = ask("New name", True)
    password = None
    if name != None:
        password = ask("New password", True)
    email = None
    if password != None:
        email = ask("New email", True)
    if email == None:
        return
    active = ask_active("Account status", allow_skip=True)
    if active == None:
        return

    if active == "skip":
        real_active = None
    else:
        real_active = active

    result = S.edit_user(username, opt(name), opt(password), opt(email), real_active, db["users"])
    _done(result, db)


def _toggle_user(db):
    username = ask("Username")
    if username != None:
        result = S.toggle_user_status(username, db["users"])
        _done(result, db)


def _view_users(db):
    users = S.list_users(db["users"])

    rows = []
    for u in users:
        if u.is_active == True:
            status = "Active"
        else:
            status = "Inactive"
        rows.append((u.name, u.username, u.role, u.email, status))

    show_table(["Name", "Username", "Role", "Email", "Status"], rows)

    answer = ask("Create a txt file with all users? (y/n)", True)
    if answer == "y" or answer == "Y":
        path = data_path("users_export.txt")
        if FileHandler.export_users_txt(path, db["users"]) == True:
            print("✔ File created: " + path)
        else:
            print("✘ Failed to create the file.")

def _add_hall(db):
    name = ask("Hall name")
    capacity = None
    if name != None:
        capacity = ask("Capacity")
    equip = None
    if capacity != None:
        equip = ask("Equipment (comma separated)", True)
    active = None
    if equip != None:
        active = ask_active("Hall status")
    if active == None:
        return

    fixed = equip.replace("\u060c", ",")
    parts = fixed.split(",")
    equipment = []
    for e in parts:
        equipment.append(e)

    result = S.add_hall(name, capacity, equipment, active, db["halls"])
    _done(result, db)


def _edit_hall(db):
    halls = S.list_halls(db["halls"])
    hall = pick("Which hall?", halls, lambda h: h.name)
    if hall == None:
        return
    print("Press Enter to leave a field unchanged.")
    new_name = ask("New name", True)
    capacity = None
    if new_name != None:
        capacity = ask("New capacity", True)
    equip = None
    if capacity != None:
        equip = ask("New equipment (comma separated)", True)
    if equip == None:
        return

    if not equip:
        equipment = None
    else:
        fixed = equip.replace("\u060c", ",")
        equipment = fixed.split(",")

    result = S.edit_hall(hall.name, opt(new_name), opt(capacity), equipment,
                         db["halls"], db["classes"])
    _done(result, db)


def _toggle_hall(db):
    halls = S.list_halls(db["halls"])

    def show_hall(h):
        if h.is_active == True:
            status = "Active"
        else:
            status = "Inactive"
        return h.name + " (" + status + ")"

    hall = pick("Which hall?", halls, show_hall)
    if hall != None:
        result = S.toggle_hall_status(hall.name, db["halls"])
        _done(result, db)


def _view_halls(db):
    halls = S.list_halls(db["halls"])

    rows = []
    for h in halls:
        equipment_text = ""
        for e in h.equipment:
            if equipment_text != "":
                equipment_text = equipment_text + ", "
            equipment_text = equipment_text + e

        if h.is_active == True:
            status = "Active"
        else:
            status = "Inactive"

        rows.append((h.name, h.capacity, equipment_text, status))

    show_table(["Name", "Capacity", "Equipment", "Status"], rows)


def _class_row(c, db):
    coach = db["users"].get(c.coach_username)

    if coach != None:
        coach_name = coach.name
    else:
        coach_name = c.coach_username

    if c.is_active == True:
        status = "Active"
    else:
        status = "Inactive"

    time_text = c.day + " " + c.time

    return (c.class_id, c.title, c.sport_type, coach_name,
            c.hall_name, time_text, c.capacity, c.capacity_remaining, status)


def _create_class(db):
    title = ask("Class title")
    sport = None
    if title != None:
        sport = ask_choice("Sport type", SPORT_TYPES)

    coach = None
    if sport != None:
        coaches = []
        all_users = S.list_users(db["users"], ROLE_COACH)
        for u in all_users:
            if u.is_active:
                coaches.append(u)
        coach = pick("Coach", coaches, lambda u: u.name + " (" + u.username + ")")

    hall = None
    if coach != None:
        halls = []
        all_halls = S.list_halls(db["halls"])
        for h in all_halls:
            if h.is_active:
                halls.append(h)
        hall = pick("Hall", halls, lambda h: h.name + " (capacity " + str(h.capacity) + ")")

    day = None
    if hall != None:
        day = ask_choice("Day", DAYS)

    time = None
    if day != None:
        time = ask("Time (e.g. 18:30)")

    capacity = None
    if time != None:
        capacity = ask("Capacity")

    if capacity == None:
        return

    result = S.create_class(title, sport, coach.username, hall.name, day, time, capacity,
                            db["users"], db["halls"], db["classes"])
    _done(result, db)


def _edit_class(db):
    cls = pick("Which class?", db["classes"], lambda x: x.class_id + " - " + x.title)
    if cls == None:
        return
    print("Press Enter to leave a field unchanged.")
    title = ask("New title", True)
    coach = None
    if title != None:
        coach = ask("New coach username", True)
    hall = None
    if coach != None:
        hall = ask("New hall name", True)
    day = None
    if hall != None:
        day = ask("New day", True)
    time = None
    if day != None:
        time = ask("New time", True)
    capacity = None
    if time != None:
        capacity = ask("New capacity", True)
    if capacity == None:
        return

    result = S.edit_class(cls.class_id, opt(title), None, opt(coach), opt(hall), opt(day),
                          opt(time), opt(capacity), db["users"], db["halls"], db["classes"])
    _done(result, db)


def _toggle_class(db):
    def show_cls(x):
        if x.is_active == True:
            status = "Active"
        else:
            status = "Inactive"
        return x.class_id + " - " + x.title + " (" + status + ")"

    cls = pick("Which class?", db["classes"], show_cls)
    if cls != None:
        result = S.toggle_class_status(cls.class_id, db["classes"])
        _done(result, db)


def _view_classes(db):
    classes = S.list_classes(db["classes"])
    rows = []
    for x in classes:
        rows.append(_class_row(x, db))
    show_table(["ID", "Title", "Sport", "Coach", "Hall", "Time", "Total capacity", "Remaining", "Status"], rows)


def _create_plan(db):
    title = ask("Title")
    months = None
    if title != None:
        months = ask("Duration (months)")
    price = None
    if months != None:
        price = ask("Amount")
    if price != None:
        result = S.create_plan(title, months, price, db["plans"])
        _done(result, db)


def _view_plans(db):
    plans = S.list_plans(db["plans"])
    rows = []
    for p in plans:
        rows.append((p.title, p.duration_months, format(p.price, ",")))
    show_table(["Title", "Duration (months)", "Amount"], rows)


def _assign_plan(db):
    members = S.list_users(db["users"], ROLE_MEMBER)
    member = pick("Member", members, lambda u: u.name + " (" + u.username + ")")

    plan = None
    if member != None:
        plans = S.list_plans(db["plans"])
        plan = pick("Plan", plans, lambda p: p.title + " - " + format(p.price, ","))

    if plan != None:
        result = S.assign_subscription(member.username, plan.title, db["users"], db["plans"],
                                       db["payments"])
        _done(result, db)


def _view_payments(db):
    payments = S.list_payments(db["payments"], db["users"])
    rows = []
    for r in payments:
        rows.append((r["member_name"], r["plan_title"], format(r["amount"], ","), r["payment_date"],
                     r["start_date"], r["end_date"], r["tracking_id"]))
    show_table(["Member", "Type", "Amount", "Payment date", "Start", "End", "Tracking number"], rows)


def _view_subscription_statuses(db):
    data = S.list_subscription_statuses(db["users"])
    show_table(["Member name", "Subscription status"], data)
    save_all(db)


def _reports(db):
    r = S.generate_reports(db["users"], db["classes"], db["payments"])
    print("\n--- Reports ---")
    print("Active members: " + str(r["active_members"]))
    print("Active coaches: " + str(r["active_coaches"]))
    print("Active classes: " + str(r["active_classes"]))
    print("Total income: " + format(r["total_income"], ","))

    answer = ask("Show advanced reports? (y/n)", True)
    if answer == "y" or answer == "Y":
        a = S.advanced_reports(db["classes"], db["payments"])
        print("Enrollments per class:", a["enrollments_per_class"])
        print("Income by plan:", a["income_by_plan"])
        print("Most popular class:", a["top_class"])