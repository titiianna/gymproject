from ui.colors import bcolors

CANCEL = "/"


def menu(title, items):
    """Numbered menu; returns the chosen number (starting at 1)."""
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
        value = input(f"{prompt} (cancel: {CANCEL}): ").strip()
        if value == CANCEL:
            return None
        if value or allow_empty:
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