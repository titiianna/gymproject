from ui.helpers import menu
from database import save_all
from ui.member_menu_funcs import (
    _profile, _programs,
    _view_balance, _top_up_wallet, _view_transactions, _pay_for_plan,
    _show_classes, _enroll_class, _cancel_class,
)
from services.member_service import MemberService as S


def member_panel(member, db):
    while True:
        c = menu(f"Member panel ({member.name})",
                 ["Profile and subscription status", "Wallet", "Classes", "Training program", "Exit"])
        if c == 1:
            _profile(member, db)
        elif c == 2:
            _wallet_menu(member, db)
        elif c == 3:
            _classes_menu(member, db)
        elif c == 4:
            _programs(member, db)
        else:
            save_all(db)
            return


def _wallet_menu(member, db):
    while True:
        c = menu("Wallet", ["View balance", "Top up wallet", "View transactions",
                            "Pay for or renew a plan", "Back"])
        if c == 1:
            _view_balance(member, db)
        elif c == 2:
            _top_up_wallet(member, db)
        elif c == 3:
            _view_transactions(member, db)
        elif c == 4:
            _pay_for_plan(member, db)
        else:
            return


def _classes_menu(member, db):
    while True:
        c = menu("Classes", ["View classes available for enrollment", "Enroll in a class",
                            "Cancel class enrollment", "My classes", "Back"])
        if c == 1:
            _show_classes(S.list_available_classes(db["classes"]), db)
        elif c == 2:
            _enroll_class(member, db)
        elif c == 3:
            _cancel_class(member, db)
        elif c == 4:
            _show_classes(member, db)
        else:
            return