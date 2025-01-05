import os

# GLOBAL CONSTANTS
MAIN_DIR = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..")
    )
DIARY_FILE: str = os.path.join(MAIN_DIR, "data", "diary_TEST.json")
CATEGORY_FILE: str = os.path.join(MAIN_DIR, "data", "cat.json")
SONG_FILE: str = os.path.join(MAIN_DIR, "data", "songs.json")
SONG_HISTORY_FILE: str = os.path.join(MAIN_DIR, "data", "songs_history.json")
JSON_INDENT: int = 4
NAN: str = "NaN"

# MENU
MENU: list[dict[str, int | str]] = [
    {
        "id": 1,
        "text": "Create entry for today",
        "script": "create_entry"
    },
    # {
    #     "id": 2,
    #     "text": "See open entries and complete diary",
    #     "script": "complete_diary"
    # },
    # {
    #     "id": 3,
    #     "text": "Edit or delete entry",
    #     "script": "edit_entry"
    # },
    # {
    #     "id": 4,
    #     "text": "Read diary",
    #     "script": "read_diary"
    # },
    # {
    #     "id": 5,
    #     "text": "View statistics",
    #     "script": "view_stats"
    # },
    # {
    #     "id": 6,
    #     "text": "Edit settings",
    #     "script": "settings"
    # },
    {
        "id": 7,
        "text": "Get another random song <3",
        "script": "random_song"
    }
]
