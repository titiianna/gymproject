from ui.colors import bcolors

CANCEL = "/"

def menu(title, items):
    while True:
        print(bcolors.OKGREEN + "\n=== " + title + " ===" + bcolors.ENDC)
        i = 1
        for item in items:
            print(str(i) + ". " + item)
            i = i + 1
        raw = input(bcolors.OKGREEN + "➜ " + bcolors.ENDC + "select[1-" + str(len(items)) + "]: ").strip()
        if raw.isdigit() == True:
            num = int(raw)
            if num >= 1 and num <= len(items):
                return num
        print(bcolors.FAIL + "Invalid option; try again." + bcolors.ENDC)

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
