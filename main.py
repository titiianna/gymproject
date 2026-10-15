import database
from services.auth_service import AuthService
from utils.constants import ROLE_ADMIN, ROLE_COACH, ROLE_MEMBER
from ui.admin_menu import admin_panel
from ui.coach_menu import coach_panel
from ui.member_menu import member_panel
from ui.helpers import ask , menu
from ui.colors import bcolors

PANELS = {ROLE_ADMIN: admin_panel, ROLE_COACH: coach_panel, ROLE_MEMBER: member_panel}


def database_init():
    return database.database_init()


def login_flow(role, db):
    while True:
        username = ask("Username")
        if username != None:
            password = ask("Password")
        else:
            password = None
        if password == None:
            return
        ok, msg, user = AuthService.login(role, username, password, db["users"])

        if ok:
            print(f"✔ {msg}")
            PANELS[role](user, db)
            return
        else:
            print(f"✘ {msg}")
  
        c = menu("What would you like to do?", [
                    "Try again", 
                    "Back",
                ])
        if c == 2:
            return


def main():
    db = database_init()
    roles = {1: ROLE_ADMIN, 2: ROLE_COACH, 3: ROLE_MEMBER}
    try:
        while True:
            try:
                c = menu("Main menu", ["Admin login", "Coach login", "Member login", "Exit"])
                if c == 4:
                    break
                login_flow(roles[c], db)
            except (KeyboardInterrupt):
                raise
            except Exception as e:
                print(bcolors.FAIL + f"error: {e}" + bcolors.ENDC)
    except (KeyboardInterrupt):
        print("/n/n" + bcolors.WARNING + "[KeyboardInterrupt] Interrupted by user." + bcolors.ENDC)
    finally:
        database.save_all(db)
    print("Goodbye!")


if __name__ == "__main__":
    main()