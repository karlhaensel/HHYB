from scripts import random_song, create_entry
from utils import tools
from utils.config import MENU


# CONSTANTS
PROGRAM: str = "HHYB - Your Diary"


# PROCEDURES
def main() -> bool:
    print("MENU")
    print("What would you like to do? Choose the corresponding number:")
    for item in MENU:
        print(f"({item["id"]}) : {item["text"]}")
    print("Enter any other character(s) to exit.")
    choice: str = input()
    for item in MENU:
        if choice == str(item["id"]):
            globals()[item["script"]].main()
            print("Press Enter to continue to menu.")
            input()
            tools.reset_terminal()
            return True
    else:
        return False


if __name__ == '__main__':
    print("*** WELCOME TO HHYB, YOUR PERSONAL DIARY! ***")
    print("Let's start with some great music!")
    random_song.main()
    # TODO: add random_cat_picture() !!!
    while True:
        if not main():  # main() caught non-id input -> exit
            break
    tools.exit_program(PROGRAM)
