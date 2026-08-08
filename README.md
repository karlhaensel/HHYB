# HHYB
- ...is a simple terminal-based diary
- with different, customisable categories,
- a few more features to come (like pretty-printed reading, editing, statistics e.g.),
- and a good taste in music (but you can change that, too!),
- which may also have influenced its name ;)

## How to use?
1. Install [Python](https://www.python.org/downloads/) 3.9 or higher (if not already satisfied)
2. Clone the repository: `git clone https://github.com/karlhaensel/na2mc`
3. Create a virtual environment: `python -m  venv .venv`
4. Activate the virtual environment:
    - on Linux/ macOS: `source .venv/bin/activate`
    - on Windows(CMD): `.venv\Scripts\activate`
    - on Windows (PowerShell): `.venv\Scripts\Activate.ps1`
5. Install dependencies: `pip install -r requirements.txt`
6. (optional, if you want to contribute) Install pre-commit hooks: `pre-commit install`
7. Run the app: `python -m hhyb.py`
