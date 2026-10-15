from ui.colors import bcolors
import getpass

CANCEL = "/"


def menu(title, items):
    while True:
        print(bcolors.OKGREEN+f"\n=== {title} ==="+bcolors.ENDC)
        for i, item in enumerate(items, 1):
            print(f"{i}. {item}")
        raw = input(bcolors.OKGREEN+"➜ "+bcolors.ENDC+f"select[1-{len(items)}]: ").strip()
        if raw.isdigit() and 1 <= int(raw) <= len(items):
            return int(raw)
        print(bcolors.FAIL+"Invalid option; try again."+bcolors.ENDC)


def ask(prompt, allow_empty=False):
    while True:
        value = input(prompt + " (cancel: " + CANCEL + "): ").strip()
        if value == CANCEL:
            return None
        if value:
            return value
        if allow_empty:
            return value
        print("Input cannot be empty.")

def ask_passwd(prompt):
    while True:
        pass_prompt = prompt + " (cancel: " + CANCEL + "): "
        passwd = getpass.getpass(prompt=pass_prompt).strip()
        if passwd == CANCEL:
            return None
        if passwd:
            return passwd
        print("Password cannot be empty.")

def pick(title, items, label):
    if len(items) == 0:
        print("Nothing to display.")
        return None

    names = []
    for i in items:
        names.append(label(i))
    names.append("Back")

    c = menu(title, names)

    if c == len(names):
        return None
    return items[c - 1]


def show_table(headers, rows):
    if len(rows) == 0:
        print("Nothing to display.")
        return
    print(" | ".join(headers))
    print("-" * 60)
    for row in rows:
        parts = []
        for x in row:
            parts.append(str(x))
        print(" | ".join(parts))


def opt(value):
    if value:
        return value
    else:
        return None


def ask_choice(prompt, options):
    options_list = list(options)
    full_list = []
    for o in options_list:
        full_list.append(o)
    full_list.append("Cancel")

    c = menu(prompt, full_list)

    if c == len(options_list) + 1:
        return None
    return options_list[c - 1]


def ask_active(prompt="Status", allow_skip=False):
    items = ["Active", "Inactive"]
    if allow_skip:
        items.append("No change")
    items.append("Cancel")

    c = menu(prompt, items)

    if items[c - 1] == "Cancel":
        return None
    if items[c - 1] == "No change":
        return "skip"
    if c == 1:
        return True
    else:
        return False