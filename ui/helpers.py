from colors import bcolors

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


