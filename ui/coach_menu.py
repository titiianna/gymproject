from ui.helpers import menu
from database import save_all
from ui.coach_menu_funcs import _view_classes, _programs

def coach_panel(coach, db):
    while True:
        c = menu("Coach panel (" + coach.name + ")",[
                "View my classes", 
                "Manage members' training programs",
                "Exit"
            ])
        if c == 1:
            _view_classes(coach, db)
        elif c == 2:
            _programs(coach, db)
        else:
            save_all(db)
            return