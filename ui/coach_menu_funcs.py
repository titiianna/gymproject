from database import save_all
from services.coach_service import CoachService as S
from ui.helpers import ask, menu, opt, pick, show_table

def _view_classes(coach, db):
    classes = S.get_coach_classes(coach.username, db["classes"])
    if len(classes) == 0:
        print("No classes are assigned to you.")
    for c in classes:
        result = S.get_class_members(coach.username, c.class_id, db["classes"], db["users"])
        members = result[2]

        names = ""
        for m in members:
            if names != "":
                names = names + ", "
            names = names + m.name
        if names == "":
            names = "-"

        if c.is_active == True:
            status = "Active"
        else:
            status = "Inactive"

        print("")
        print("[" + c.class_id + "] " + c.title + " | " + c.sport_type + " | " + c.day + " " + c.time + " | " + c.hall_name + " | " + "Capacity " + str(c.capacity) + " | " + status)
        print("  Enrolled members: " + names)


def _ask_exercise(defaults=None):
    name = ask("Exercise name", defaults is not None)

    sets_ = None
    if name != None:
        sets_ = ask("Sets", defaults is not None)

    reps = None
    if sets_ != None:
        reps = ask("Reps", defaults is not None)

    rest = None
    if reps != None:
        rest = ask("Rest time (seconds)", defaults is not None)

    desc = None
    if rest != None:
        desc = ask("Description", True)

    if desc == None:
        return None

    if defaults:
        real_name = opt(name)
    else:
        real_name = name

    if defaults:
        real_sets = opt(sets_)
    else:
        real_sets = sets_

    if defaults:
        real_reps = opt(reps)
    else:
        real_reps = reps

    if defaults:
        real_rest = opt(rest)
    else:
        real_rest = rest

    if desc or not defaults:
        real_desc = desc
    else:
        real_desc = None

    return {"name": real_name, "sets": real_sets,
            "reps": real_reps,
            "rest_seconds": real_rest,
            "description": real_desc}


def _show_program(program):
    rows = []
    i = 1
    for e in program.exercises:
        rows.append((i, e.name, e.sets, e.reps, e.rest_seconds, e.description))
        i = i + 1
    show_table(["#", "Exercise", "Sets", "Reps", "Rest (seconds)", "Description"], rows)


def _programs(coach, db):
    classes = S.get_coach_classes(coach.username, db["classes"])
    cls = pick("Choose a class", classes,
               lambda c: c.class_id + " - " + c.title)
    if cls == None:
        return

    result = S.get_class_members(coach.username, cls.class_id, db["classes"], db["users"])
    ok = result[0]
    msg = result[1]
    members = result[2]

    member = pick("Choose a member", members, lambda m: m.name + " (" + m.username + ")")
    if member == None:
        return

    while True:
        result = S.get_program(coach.username, cls.class_id, member.username,
                               db["classes"], db["programs"])
        ok = result[0]
        program = result[2]

        if ok == False:
            c = menu("This member has no program yet", ["Create program", "Back"])
            if c == 2:
                return

            exercises = []
            while True:
                ex = _ask_exercise()
                if ex == None:
                    break
                exercises.append(ex)
                if menu("Add another exercise?", ["Yes", "No"]) == 2:
                    break

            if len(exercises) > 0:
                res = S.add_training_program(cls.class_id, member.username, exercises,
                                             coach.username, db["classes"], db["users"], db["programs"])
                if res[0] == True:
                    print("✔ " + res[1])
                else:
                    print("✘ " + res[1])
                if res[0] == True:
                    save_all(db)
            continue

        c = menu("Training program", ["View program", "Add exercise", "Edit exercise", "Back"])
        if c == 1:
            _show_program(program)
        elif c == 2:
            ex = _ask_exercise()
            if ex != None:
                res = S.add_exercise(cls.class_id, member.username, ex, coach.username,
                                     db["classes"], db["programs"])
                if res[0] == True:
                    print("✔ " + res[1])
                else:
                    print("✘ " + res[1])
                if res[0] == True:
                    save_all(db)
        elif c == 3:
            _show_program(program)
            num = ask("Exercise number")
            if num == None or num.isdigit() == False:
                continue
            print("Press Enter to leave a field unchanged.")
            data = _ask_exercise(defaults=True)
            if data != None:
                res = S.edit_exercise(cls.class_id, member.username, int(num) - 1, data,
                                      coach.username, db["classes"], db["programs"])
                if res[0] == True:
                    print("✔ " + res[1])
                else:
                    print("✘ " + res[1])
                if res[0] == True:
                    save_all(db)
        else:
            return