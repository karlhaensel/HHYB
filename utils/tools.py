import os
import shutil
from datetime import datetime
from utils.config import MAIN_DIR


def backup_file(file) -> str:
    now: str = datetime.now().strftime("%y%m%d%H%M%S")
    path_without_ext, ext = os.path.splitext(file)
    file_backup = os.path.join(
        MAIN_DIR, "backup",
        f"{os.path.basename(path_without_ext)}_{now}{ext}")
    return shutil.copy2(file, file_backup)


def backup_data(*args) -> None:
    print(args)
    for dat in args:
        file = os.path.join(MAIN_DIR, "data", f"{dat}.json")
        backup_file(file)


# TODO: add restore_data/restore_file
# TODO: add delete_old_backup_data/tidy_backup (remove duplicates e.g.)


def reset_terminal() -> None:
    if os.name == "nt":  # Windows system
        os.system("cls")
    else:  # Unix-based system
        os.system("clear")


def exit_program(program: str) -> None:
    print(f"Thank you for using \"{program}\" and goodbye!")
    input()
    exit()
