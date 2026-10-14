from database import save_all
from services.admin_service import AdminService as S
from utils.constants import DAYS, ROLE_COACH, ROLE_MEMBER, SPORT_TYPES, data_path
from utils.file_handler import FileHandler
from ui.helpers import ask, ask_active, ask_choice, opt, show_table


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