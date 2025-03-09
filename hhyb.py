from scripts import random_song, create_entry
from utils import tools
from utils.config import MENU


# CONSTANTS
PROGRAM: str = "HHYB - Your Diary"


# PROCEDURES
def main() -> bool:
    # TODO: pretty print
    print("MENU")
    print("What would you like to do? Choose the corresponding number:")
    for item in MENU:
        print(f"({item["id"]}) : {item["text"]}")
    print("Enter any other character(s) to exit.")
    choice: str = input()
    for item in MENU:
        if choice == str(item["id"]):
            tools.reset_terminal()
            globals()[item["script"]].main()
            print("Press Enter to continue to menu.")
            input()
            tools.reset_terminal()
            return True
    else:
        return False


if __name__ == '__main__':
    # TODO: pretty print
    tools.reset_terminal()  # starting fresh :)
    print("*** WELCOME TO HHYB, YOUR PERSONAL DIARY! ***")
    print("Let's start with some great music!")
    random_song.main()
    print("What a loevely start! Continue to menu with Enter.")
    input()
    # TODO: add random_cat_picture() !!!
    # TODO: add random_poem and/or random_quote()
    while True:
        tools.reset_terminal()  # clear terminal before every menu call
        if not main():  # main() caught non-id input -> exit
            break
    tools.exit_program(PROGRAM)
