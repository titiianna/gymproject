from services.auth_service import AuthService
from utils.constants import ROLE_ADMIN, ROLE_COACH, ROLE_MEMBER
from ui.admin_menu import admin_panel
from ui.coach_menu import coach_panel
from ui.member_menu import member_panel
from ui.helpers import ask , menu

PANELS = {ROLE_ADMIN: admin_panel, ROLE_COACH: coach_panel, ROLE_MEMBER: member_panel}

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
        else:
            print(f"✘ {msg}")

        if ok:
            PANELS[role](user, db)
            return
        
        c = menu("What would you like to do?", [
                    "Try again", 
                    "Back",
                ])
        if c == 2:
            return