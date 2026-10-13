from database import save_all
from services.member_service import MemberService as S
from ui.helpers import menu, show_table


def member_panel(member, db):
    while True:
        c = menu("Member panel (" + member.name + ")",
                 ["Profile and subscription status", "Wallet", "Classes", "Training program", "Exit"])

        if c == 1:
            p = S.get_profile(member.username, db["users"])

            print("Name: " + str(p["name"]))
            print("Username: " + str(p["username"]))
            print("Email: " + str(p["email"]))
            print("Account status: " + str(p["account_status"]))
            print("Plan: " + str(p["subscription_type"]))
            print("Start date: " + str(p["subscription_start"]))
            print("End date: " + str(p["subscription_end"]))
            print("Subscription status: " + str(p["subscription_status"]))

        elif c == 2:
            _wallet(member, db)

        elif c == 3:
            _classes(member, db)

        elif c == 4:
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

        else:
            save_all(db)
            return