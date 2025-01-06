import os
import shutil
from datetime import datetime
from utils.config import MAIN_DIR


def backup_file(file) -> str:
    now: str = datetime.now().strftime("%Y%m%d%H%M%S")
    base, ext = os.path.splitext(file)
    file_backup = os.path.join(MAIN_DIR, "backup",
                               f"{os.path.basename(base)}_{now}{ext}")
    return shutil.copy2(file, file_backup)


def backup_data(*args) -> None:
    for dat in args:
        file = os.path.join(MAIN_DIR, "data", dat, ".json")
        backup_file(file)


# TODO: add restore_data/restore_file and delete_old_backup_data functions


def reset_terminal() -> None:
    if os.name == "nt":  # Windows system
        os.system("cls")
    else:  # Unix-based system
        os.system("clear")


def exit_program(program: str) -> None:
    print(f"Thank you for using \"{program}\" and goodbye!")
    input()
    exit()
