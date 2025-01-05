import os


def reset_terminal() -> None:
    if os.name == "nt":  # Windows system
        os.system("cls")
    else:  # Unix-based system
        os.system("clear")


def exit_program(program: str) -> None:
    print(f"Thank you for using \"{program}\" and goodbye!")
    input()
    exit()
