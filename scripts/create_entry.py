import json
from datetime import datetime, timedelta
if __name__ != '__main__':
    from utils.config import CATEGORY_FILE, DIARY_FILE, NAN, JSON_INDENT
    from utils import tools


# CONSTANTS
PROGRAM: str = "HHYB - Create Entry"


# FUNCTIONS
def get_entry(
        cat: dict[str, str | list[str] | int | float]) -> str | int | float:
    answer: str = input(cat["prompt"])
    if (answer == "-") and (cat["type"] in ["int", "float"]):
        return NAN
    match cat["type"]:
        case "choice":
            if (answer in cat["options"]) or (answer == "-"):
                return answer
            else:
                print(f"ERROR: Please choose one of the following options",
                      f"(or \"-\" to skip): {cat["options"]}")
                return get_entry(cat)
        case "int":
            try:
                number: int = int(answer)
            except ValueError:
                print("ERROR: Please enter an integer or skip with '-'.")
                return get_entry(cat)
            if cat["min"] <= number <= cat["max"]:
                return number
            else:
                print(f"ERROR: Please enter an integer between {cat['min']}",
                      f"and {cat['max']}.")
                return get_entry(cat)
        case "float":
            try:
                number: float = float(answer)
            except:
                print("ERROR: Please enter a number or skip with '-'.")
                return get_entry(cat)
            if cat["min"] <= number <= cat["max"]:
                return number
            else:
                print(f"ERROR: Please enter a number between {cat['min']}",
                      f"and {cat['max']}.")
                return get_entry(cat)
        case _:  # str (default)
            return answer


def main() -> None:
    completely_new: bool = False
    try:
        with open(DIARY_FILE, "r", encoding="utf-8") as file:
            diary_data = json.load(file)
    except FileNotFoundError:
        print("ERROR: No diary found. Creating new diary.")
        diary_data = []
        completely_new = True
    today = datetime.now().strftime("%Y-%m-%d")
    if not completely_new:
        last_entry_date = diary_data[-1]["date"]
        yesterday = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")
        if last_entry_date < yesterday:
            print("You did not enter something yesterday. Someday there will",
                  "be an option to edit now. But not yet so...(sorry!)")
            # TODO: go to edit_entry or sth like that
        elif last_entry_date == today:
            print("You already entered a diary entry for today:")
            print(json.dumps(diary_data[-1], indent=0, ensure_ascii=False))
            # TODO: pretty print...
            if change := input("Do you want to change it (y/n)?") == "y":
                diary_data.pop()
            else:
                print("Okay, no changes it is.")
                tools.exit_program(PROGRAM)
    print("Please answer the following prompts for your diary. Skip with '-'.")
    new_entry: dict[str, str | int | float] = {}
    new_entry["date"] = today
    with open(CATEGORY_FILE, "r", encoding="utf-8-sig") as file:
        cats = json.load(file)
    for cat in cats:
        new_entry[cat["name"]] = get_entry(cat)
    diary_data.append(new_entry)
    with open(DIARY_FILE, "w", encoding="utf-8") as file:
        json.dump(diary_data, file, ensure_ascii=False, indent=JSON_INDENT)


if __name__ == '__main__':
    print("I am just a module. Please choose me from HHBY's main menu.")
    input()
