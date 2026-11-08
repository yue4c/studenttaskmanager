# Smart Student Task Manager – Unit V

Student: Yuepel | ID: 08230241 | Framework: PyQt6 | Database: SQLite

## Requirements

Windows, macOS or Linux; Python 3.10 or later. Tested for database logic using Python 3; actual PyQt6 GUI execution must be verified on your computer.

## Install and run (Windows PowerShell)

```powershell
cd partB
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python main.py
```

If PowerShell blocks activation, run without activation:

```powershell
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe main.py
```

## How to use

1. Enter a task title (required), optional description, priority, and due date.
2. Press **Add Task**. The item appears in the table and is saved in `tasks.db`.
3. Click a table row to load the task; change fields and press **Save Changes**.
4. Click **Toggle Complete** to change the task's status.
5. Click **Delete Selected** to open a confirmation dialogue.
6. Search by text or filter by priority/status. The progress bar shows the percentage of all tasks completed.
7. Close and reopen the app: the SQLite records persist.

## Files

- `main.py`: starts Qt and opens the application
- `ui.py`: interface, widgets, layouts, events and validation
- `database.py`: all SQL data operations
- `tasks.db`: persistent SQLite database with sample records
- `requirements.txt`: pinned dependencies

## Data schema

`tasks(id INTEGER PRIMARY KEY, title TEXT NOT NULL, description TEXT, priority TEXT, due_date TEXT (YYYY-MM-DD), completed INTEGER (0/1))`

## Assignment checklist

- Main window + File/Help menus: yes
- 8+ widget types: QLabel, QLineEdit, QTextEdit, QComboBox, QDateEdit, QCheckBox, QPushButton, QTableWidget, QProgressBar, QGroupBox
- 2+ layouts: QVBoxLayout, QHBoxLayout, QGridLayout
- 5+ handled events: add, update, delete, toggle, clear, text search, filter change, row select, menu actions
- Dialog: About, validation warnings, confirmation
- Input validation: blank/overlong title, overlong description
- Persistence: SQLite `tasks.db`
- Custom styles: Qt Style Sheets
- UI/data separation: `ui.py` and `database.py`

## Screenshots required for submission

Capture screenshots of your app running on your own Windows device with the window title visible:

1. Full task manager with sample tasks
2. Selected task loaded into the edit form
3. Validation popup from pressing Add Task with a blank title
4. Delete confirmation popup
5. Search or filtering in action
6. Help > About (shows name and student ID)

## Integrity and viva

Understand and personalise the program. Disclose ChatGPT assistance for the initial code structure and debugging in your report. Do not report a test as passed unless you ran it yourself.
