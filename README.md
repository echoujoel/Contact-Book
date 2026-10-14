# Contact-Book

A small, persistent command-line contact management system written in Python. Use the numbered menu to add, view, search, and delete contacts. The program saves contacts locally in `contacts.json` so they are available the next time it runs.

## Requirements

- Python 3.9 or newer
- No third-party packages

## Run the program

Open a terminal in this repository and run:

```bash
python contact_manager.py
```

If your system uses `python3` as the Python command, run:

```bash
python3 contact_manager.py
```

## Menu options

1. **Add contact** — enter a name and phone number. Names are matched without regard to case, preventing duplicates such as `Sam Lee` and `sam lee`.
2. **View contacts** — display all contacts in alphabetical order, one per line.
3. **Search contact** — find a phone number by name. Matching ignores letter case and extra spaces.
4. **Delete contact** — find a contact and confirm before it is removed.
5. **Exit** — close the program gracefully.

Names and phone numbers cannot be blank. A missing contact file is created automatically the first time you add a contact. If the existing data file cannot be read, the program reports the problem instead of silently replacing the file.

## Data and privacy

Contact data is stored in `contacts.json` beside the program and stays on the computer where you run it. The included `.gitignore` excludes that file from Git so personal contact details are not committed with the source code. Back up `contacts.json` separately if you want to keep a copy.

## Files

- `contact_manager.py` — menu, contact operations, and JSON storage
- `README.md` — setup and usage instructions
- `.gitignore` — excludes local contact data and Python cache files

