from ui.helpers import menu
from database import save_all
from ui.admin_menu_funcs import (
    _add_user, _edit_user, _toggle_user, _view_users,
    _add_hall, _edit_hall, _toggle_hall, _view_halls,
    _create_class, _edit_class, _toggle_class, _view_classes,
    _create_plan, _view_plans, _assign_plan, _view_payments,
    _view_subscription_statuses, _reports,
)


def admin_panel(admin, db):
    while True:
        c = menu("Admin panel (" + admin.name + ")", [
            "Manage users",
            "Manage halls",
            "Manage classes",
            "Manage plans and payments",
            "View reports",
            "Exit",
        ])
        if c == 1:
            _users_menu(db)
        elif c == 2:
            _halls_menu(db)
        elif c == 3:
            _classes_menu(db)
        elif c == 4:
            _subs_menu(db)
        elif c == 5:
            _reports(db)
        else:
            save_all(db)
            return


def _users_menu(db):
    while True:
        c = menu("Manage users", [
            "Add user", 
            "Edit user", 
            "Activate/deactivate",
            "View users", 
            "Back",
        ])
        if c == 1:
            _add_user(db)
        elif c == 2:
            _edit_user(db)
        elif c == 3:
            _toggle_user(db)
        elif c == 4:
            _view_users(db)
        else:
            return


def _halls_menu(db):
    while True:
        c = menu("Manage halls", [
            "Add hall", 
            "Edit hall", 
            "Activate/deactivate",
            "View halls", 
            "Back",
        ])
        if c == 1:
            _add_hall(db)
        elif c == 2:
            _edit_hall(db)
        elif c == 3:
            _toggle_hall(db)
        elif c == 4:
            _view_halls(db)
        else:
            return


def _classes_menu(db):
    while True:
        c = menu("Manage classes", [
            "Create class", 
            "Edit class", 
            "Activate/deactivate",
            "View classes", 
            "Back",
        ])
        if c == 1:
            _create_class(db)
        elif c == 2:
            _edit_class(db)
        elif c == 3:
            _toggle_class(db)
        elif c == 4:
            _view_classes(db)
        else:
            return


def _subs_menu(db):
    while True:
        c = menu("Manage plans and payments",[
            "Define a new plan",
            "View plans",
            "Assign plan to member",
            "View payments",
            "Members subscription status",
            "Back",
        ])
        if c == 1:
            _create_plan(db)
        elif c == 2:
            _view_plans(db)
        elif c == 3:
            _assign_plan(db)
        elif c == 4:
            _view_payments(db)
        elif c == 5:
            _view_subscription_statuses(db)
        else:
            return