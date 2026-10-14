from database import save_all
from services.member_service import MemberService as S
from ui.helpers import menu, show_table, pick, ask 


def member_panel(member, db):
    while True:
        c = menu(f"Member panel {member.name}",
                 ["Profile and subscription status", "Wallet", "Classes", "Training program", "Exit"])

        if c == 1:
            _profile(member, db)

        elif c == 2:
            _wallet(member, db)

        elif c == 3:
            _classes(member, db)

        elif c == 4:
            _program(member, db)

        else:
            save_all(db)
            return