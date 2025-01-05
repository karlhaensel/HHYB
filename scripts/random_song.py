if __name__ != '__main__':
    import json
    from random import choice
    from utils.config import SONG_FILE, SONG_HISTORY_FILE, JSON_INDENT


# CONSTANTS
PROGRAM: str = "HHYB - Your Random Song"


# FUNCTIONS
def get_songdata(path: str) -> list[dict[str, str]]:
    with open(path, "r", encoding="utf-8-sig") as file:
        return json.load(file)


def main() -> None:
    songs: list[dict[str, str]] = get_songdata(SONG_FILE)
    try:
        songs_history: list[dict[str, str]] = get_songdata(SONG_HISTORY_FILE)
    except FileNotFoundError:
        songs_history = []  # history file will be created later
    if songs == songs_history:  # CAVE: both have to be sorted by title!
        songs_history = []  # reset history
    song: dict[str, str] = choice(songs)
    if song not in songs_history:
        songs_history.append(song)
        print(f"There is your random {song["artist"]} song:",
              f"\"{song["title"]}\" (from \"{song["from"]}\") <3")
        with open(SONG_HISTORY_FILE, "w", encoding="utf-8-sig") as file:
            json.dump(
                sorted(songs_history, key=lambda x: x["title"]),
                file, ensure_ascii=False, indent=JSON_INDENT
            )
    else:
        main()


if __name__ == '__main__':
    print("I am just a module. Please choose me from HHBY's main menu.")
    input()
