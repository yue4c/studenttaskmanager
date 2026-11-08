
"""SQLite database for Smart Student Task Manager."""

import sqlite3
from pathlib import Path
from contextlib import contextmanager


# Database stored in the same folder as this file
DB_PATH = Path(__file__).resolve().parent / "tasks.db"


class TaskRepository:

    def __init__(self, path=DB_PATH):
        self.path = str(path)
        self.create_table()

    # -------- DATABASE CONNECTION --------

    @contextmanager
    def _connect(self):
        connection = sqlite3.connect(self.path)
        connection.row_factory = sqlite3.Row

        try:
            with connection:
                yield connection
        finally:
            connection.close()

    # -------- CREATE DATABASE TABLE --------

    def create_table(self):
        with self._connect() as con:
            con.execute("""
                CREATE TABLE IF NOT EXISTS tasks (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    title TEXT NOT NULL,
                    description TEXT NOT NULL DEFAULT '',
                    priority TEXT NOT NULL
                        CHECK(priority IN ('High', 'Medium', 'Low')),
                    due_date TEXT NOT NULL,
                    completed INTEGER NOT NULL DEFAULT 0
                        CHECK(completed IN (0, 1))
                )
            """)

    # -------- ADD NEW TASK --------

    def add(
        self, title, description,
        priority, due_date, completed=False
    ):
        with self._connect() as con:
            cursor = con.execute(
                """
                INSERT INTO tasks
                (title, description, priority, due_date, completed)
                VALUES (?, ?, ?, ?, ?)
                """,
                (
                    title,
                    description,
                    priority,
                    due_date,
                    int(completed)
                )
            )

            return cursor.lastrowid

    # -------- UPDATE EXISTING TASK --------

    def update(
        self, task_id, title, description,
        priority, due_date, completed
    ):
        with self._connect() as con:
            cursor = con.execute(
                """
                UPDATE tasks
                SET title = ?,
                    description = ?,
                    priority = ?,
                    due_date = ?,
                    completed = ?
                WHERE id = ?
                """,
                (
                    title,
                    description,
                    priority,
                    due_date,
                    int(completed),
                    task_id
                )
            )

            return cursor.rowcount

    # -------- DELETE TASK --------

    def delete(self, task_id):
        with self._connect() as con:
            cursor = con.execute(
                "DELETE FROM tasks WHERE id = ?",
                (task_id,)
            )

            return cursor.rowcount

    # -------- UPDATE COMPLETION STATUS --------

    def set_completed(self, task_id, completed):
        with self._connect() as con:
            cursor = con.execute(
                """
                UPDATE tasks
                SET completed = ?
                WHERE id = ?
                """,
                (int(completed), task_id)
            )

            return cursor.rowcount

    # -------- SEARCH AND FILTER TASKS --------

    def all(self, search="", priority="All", status="All"):

        sql = "SELECT * FROM tasks WHERE 1=1"
        values = []

        # Search task title or description
        if search.strip():
            sql += """
                AND (title LIKE ? OR description LIKE ?)
            """

            term = f"%{search.strip()}%"
            values.extend([term, term])

        # Filter by priority
        if priority != "All":
            sql += " AND priority = ?"
            values.append(priority)

        # Filter by completion status
        if status == "Completed":
            sql += " AND completed = 1"

        elif status == "Pending":
            sql += " AND completed = 0"

        # Display pending tasks first, sorted by deadline
        sql += """
            ORDER BY completed ASC, due_date ASC, id DESC
        """

        with self._connect() as con:
            rows = con.execute(sql, values).fetchall()
            return [dict(row) for row in rows]

    # -------- TASK TOTALS --------

    def totals(self):

        with self._connect() as con:
            row = con.execute("""
                SELECT
                    COUNT(*) AS total,
                    COALESCE(SUM(completed), 0) AS done
                FROM tasks
            """).fetchone()

            return row["total"], row["done"]


# -------- SAMPLE TASKS --------

def add_sample_tasks_if_empty(repository):
    """Insert sample tasks only if the database is empty."""

    if repository.totals()[0] > 0:
        return

    sample_tasks = [
        (
            "Complete Python GUI assignment",
            "Finish Part B and test the application",
            "High",
            "2026-11-06",
            False
        ),
        (
            "Prepare framework comparison",
            "Review licensing and layout systems",
            "Medium",
            "2026-11-04",
            True
        ),
        (
            "Capture Hello World screenshots",
            "Run three GUI programs and take screenshots",
            "High",
            "2026-11-05",
            False
        ),
        (
            "Review class notes",
            "Read Unit V GUI concepts",
            "Low",
            "2026-11-07",
            False
        )
    ]

    for task in sample_tasks:
        repository.add(*task)
