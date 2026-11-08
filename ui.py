"""PyQt6 interface for Smart Student Task Manager."""

from PyQt6.QtCore import QDate, Qt
from PyQt6.QtGui import QAction, QColor
from PyQt6.QtWidgets import (
    QAbstractItemView, QComboBox, QDateEdit, QDialog,
    QGridLayout, QGroupBox, QHBoxLayout, QHeaderView,
    QLabel, QLineEdit, QMainWindow, QMessageBox,
    QProgressBar, QPushButton, QTableWidget,
    QTableWidgetItem, QTextEdit, QVBoxLayout,
    QWidget, QCheckBox, QScrollArea, QSizePolicy, QLayout
)

from database import TaskRepository


# ---------------- APPLICATION THEME ----------------

STYLE = """
QMainWindow, QWidget {
    background: #0d1426;
    color: #f0f5ff;
    font-family: 'Segoe UI';
    font-size: 13px;
}

QGroupBox {
    border: 1px solid #354a6c;
    border-radius: 10px;
    margin-top: 12px;
    font-weight: bold;
}

QGroupBox::title {
    subcontrol-origin: margin;
    left: 14px;
    padding: 0 6px;
}

QLineEdit, QTextEdit, QComboBox, QDateEdit {
    background: #192640;
    border: 1px solid #425979;
    border-radius: 6px;
    color: white;
    padding: 7px;
}

QPushButton {
    background: #2563eb;
    color: white;
    border: none;
    border-radius: 7px;
    padding: 9px 12px;
    font-weight: bold;
}

QPushButton:hover {
    background: #3b82f6;
}

QPushButton#deleteButton {
    background: #b83245;
}

QPushButton#clearButton {
    background: #475569;
}

QTableWidget {
    background: #131f36;
    alternate-background-color: #1c2b46;
    gridline-color: #344765;
    selection-background-color: #2563eb;
}

QHeaderView::section {
    background: #243755;
    color: white;
    padding: 8px;
    border: 1px solid #344765;
}

QProgressBar {
    background: #1e293b;
    border: 1px solid #475569;
    border-radius: 6px;
    text-align: center;
    min-height: 19px;
}

QProgressBar::chunk {
    background: #10b981;
    border-radius: 5px;
}

QMenuBar, QMenu, QStatusBar {
    background: #14213a;
    color: white;
}

QCalendarWidget QWidget {
    background: #192640;
}
"""


class TaskManagerWindow(QMainWindow):

    def __init__(self, repository=None):
        super().__init__()

        self.repo = (
            repository if repository is not None
            else TaskRepository()
        )

        self.selected_task_id = None

        self.setWindowTitle(
            "Smart Student Task Manager | Yuepel | 08230241"
        )

        self.resize(1150, 790)
        self.setMinimumSize(850, 550)
        self.setStyleSheet(STYLE)

        self.setup_ui()
        self.connect_events()
        self.refresh_tasks()

    # ---------------- MAIN INTERFACE ----------------

    def setup_ui(self):

        file_menu = self.menuBar().addMenu("File")

        refresh_action = QAction("Refresh", self)
        refresh_action.triggered.connect(self.refresh_tasks)
        file_menu.addAction(refresh_action)

        exit_action = QAction("Exit", self)
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)

        help_menu = self.menuBar().addMenu("Help")

        about_action = QAction("About", self)
        about_action.triggered.connect(self.show_about)
        help_menu.addAction(about_action)

        # A scroll area prevents form rows being squeezed when the
        # available screen height becomes too small.
        scroll_area = QScrollArea(self)
        scroll_area.setWidgetResizable(True)
        scroll_area.setFrameShape(QScrollArea.Shape.NoFrame)
        scroll_area.setHorizontalScrollBarPolicy(
            Qt.ScrollBarPolicy.ScrollBarAsNeeded
        )
        self.setCentralWidget(scroll_area)

        central = QWidget()
        central.setMinimumWidth(810)
        scroll_area.setWidget(central)

        outer = QVBoxLayout(central)
        outer.setContentsMargins(20, 14, 20, 14)
        outer.setSpacing(10)
        # Honour the minimum space required by all widgets rather
        # than compressing them into overlapping rows.
        outer.setSizeConstraint(QLayout.SizeConstraint.SetMinimumSize)

        heading = QLabel("SMART STUDENT TASK MANAGER")
        heading.setStyleSheet(
            "font-size: 24px; font-weight: bold; "
            "color: #60a5fa;"
        )

        outer.addWidget(heading)
        outer.addWidget(
            QLabel(
                "Organise assignments | Manage deadlines | "
                "Track progress"
            )
        )

        # ---------------- TASK DETAILS FORM ----------------

        form_box = QGroupBox("Task Details")
        form_box.setMinimumHeight(300)
        form_box.setSizePolicy(
            QSizePolicy.Policy.Preferred,
            QSizePolicy.Policy.Fixed
        )

        form = QGridLayout(form_box)
        form.setContentsMargins(18, 26, 18, 14)
        form.setHorizontalSpacing(14)
        form.setVerticalSpacing(10)

        self.title_input = QLineEdit()
        self.title_input.setPlaceholderText(
            "e.g., Complete Python assignment"
        )
        self.title_input.setMinimumHeight(38)

        self.description_input = QTextEdit()
        self.description_input.setPlaceholderText(
            "Optional task description"
        )
        self.description_input.setFixedHeight(75)

        self.priority_input = QComboBox()
        self.priority_input.addItems([
            "High", "Medium", "Low"
        ])
        self.priority_input.setCurrentText("Medium")
        self.priority_input.setMinimumHeight(38)

        self.date_input = QDateEdit()
        self.date_input.setCalendarPopup(True)
        self.date_input.setDisplayFormat("dd MMM yyyy")
        self.date_input.setDate(QDate.currentDate())
        self.date_input.setMinimumHeight(38)

        self.completed_input = QCheckBox("Completed")

        # Task title row
        form.addWidget(QLabel("Task Title *"), 0, 0)
        form.addWidget(self.title_input, 0, 1, 1, 3)

        # Description row
        form.addWidget(QLabel("Description"), 1, 0)
        form.addWidget(
            self.description_input, 1, 1, 1, 3
        )

        # Priority and date row
        form.addWidget(QLabel("Priority"), 2, 0)
        form.addWidget(self.priority_input, 2, 1)

        form.addWidget(QLabel("Due Date"), 2, 2)
        form.addWidget(self.date_input, 2, 3)

        # Completed checkbox row
        form.addWidget(self.completed_input, 3, 1)

        # Layout spacing
        form.setColumnStretch(1, 2)
        form.setColumnStretch(3, 2)

        form.setRowMinimumHeight(0, 40)
        form.setRowMinimumHeight(1, 78)
        form.setRowMinimumHeight(2, 40)
        form.setRowMinimumHeight(3, 30)

        outer.addWidget(form_box, 0)

        # ---------------- ACTION BUTTONS ----------------

        actions = QHBoxLayout()

        self.add_button = QPushButton("+ Add Task")
        self.update_button = QPushButton("Save Changes")
        self.complete_button = QPushButton("Toggle Complete")
        self.delete_button = QPushButton("Delete Selected")
        self.clear_button = QPushButton("Clear Form")

        self.delete_button.setObjectName("deleteButton")
        self.clear_button.setObjectName("clearButton")

        for button in (
            self.add_button,
            self.update_button,
            self.complete_button,
            self.delete_button,
            self.clear_button
        ):
            actions.addWidget(button)

        outer.addLayout(actions)

        # ---------------- SEARCH AND FILTER ----------------

        filters = QHBoxLayout()

        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText(
            "Search by title or description..."
        )

        self.filter_priority = QComboBox()
        self.filter_priority.addItems([
            "All", "High", "Medium", "Low"
        ])

        self.filter_status = QComboBox()
        self.filter_status.addItems([
            "All", "Pending", "Completed"
        ])

        filters.addWidget(QLabel("Search"))
        filters.addWidget(self.search_input, 4)

        filters.addWidget(QLabel("Priority"))
        filters.addWidget(self.filter_priority, 1)

        filters.addWidget(QLabel("Status"))
        filters.addWidget(self.filter_status, 1)

        outer.addLayout(filters)

        # ---------------- TASK TABLE ----------------

        self.table = QTableWidget(0, 5)

        self.table.setHorizontalHeaderLabels([
            "ID", "Task Title", "Priority",
            "Due Date", "Status"
        ])

        self.table.setSelectionBehavior(
            QAbstractItemView.SelectionBehavior.SelectRows
        )

        self.table.setSelectionMode(
            QAbstractItemView.SelectionMode.SingleSelection
        )

        self.table.setEditTriggers(
            QAbstractItemView.EditTrigger.NoEditTriggers
        )

        self.table.setAlternatingRowColors(True)
        self.table.verticalHeader().setVisible(False)

        self.table.horizontalHeader().setSectionResizeMode(
            1, QHeaderView.ResizeMode.Stretch
        )

        for col, width in [
            (0, 60),
            (2, 115),
            (3, 140),
            (4, 125)
        ]:
            self.table.setColumnWidth(col, width)

        self.table.setMinimumHeight(220)
        self.table.setSizePolicy(
            QSizePolicy.Policy.Expanding,
            QSizePolicy.Policy.Expanding
        )

        outer.addWidget(self.table, 1)

        # ---------------- PROGRESS SECTION ----------------

        bottom = QHBoxLayout()

        self.summary_label = QLabel(
            "Total: 0 | Completed: 0 | Pending: 0"
        )

        self.progress = QProgressBar()
        self.progress.setRange(0, 100)

        bottom.addWidget(self.summary_label, 1)
        bottom.addWidget(self.progress, 1)

        outer.addLayout(bottom)

        self.chart_button = QPushButton(
            "View Progress Chart"
        )

        outer.addWidget(self.chart_button)

        self.statusBar().showMessage(
            "Ready — select a task to edit it."
        )

    # ---------------- SIGNALS AND SLOTS ----------------

    def connect_events(self):

        self.add_button.clicked.connect(self.add_task)

        self.update_button.clicked.connect(self.update_task)

        self.delete_button.clicked.connect(self.delete_task)

        self.complete_button.clicked.connect(
            self.toggle_completed
        )

        self.clear_button.clicked.connect(self.clear_form)

        self.search_input.textChanged.connect(
            self.refresh_tasks
        )

        self.filter_priority.currentTextChanged.connect(
            self.refresh_tasks
        )

        self.filter_status.currentTextChanged.connect(
            self.refresh_tasks
        )

        self.table.itemSelectionChanged.connect(
            self.load_selected_task
        )

        self.chart_button.clicked.connect(
            self.show_progress_chart
        )

    # ---------------- INPUT VALIDATION ----------------

    def collect_form(self):

        title = self.title_input.text().strip()

        description = (
            self.description_input.toPlainText().strip()
        )

        if not title:
            QMessageBox.warning(
                self, "Invalid Input",
                "Please enter a task title."
            )
            self.title_input.setFocus()
            return None

        if len(title) > 100:
            QMessageBox.warning(
                self, "Invalid Input",
                "Task title must not exceed 100 characters."
            )
            return None

        if len(description) > 500:
            QMessageBox.warning(
                self, "Invalid Input",
                "Description must not exceed 500 characters."
            )
            return None

        return (
            title,
            description,
            self.priority_input.currentText(),
            self.date_input.date().toString("yyyy-MM-dd"),
            self.completed_input.isChecked()
        )

    # ---------------- ADD TASK ----------------

    def add_task(self):

        values = self.collect_form()

        if values is None:
            return

        try:
            self.repo.add(*values)

        except Exception as error:
            self.show_database_error(error)
            return

        self.clear_form()
        self.refresh_tasks()

        self.statusBar().showMessage(
            "Task added successfully!", 5000
        )

    # ---------------- UPDATE TASK ----------------

    def update_task(self):

        if self.selected_task_id is None:
            QMessageBox.information(
                self, "Select Task",
                "Please select a task to update."
            )
            return

        values = self.collect_form()

        if values is None:
            return

        try:
            self.repo.update(
                self.selected_task_id, *values
            )

        except Exception as error:
            self.show_database_error(error)
            return

        self.clear_form()
        self.refresh_tasks()

        self.statusBar().showMessage(
            "Task updated successfully!", 5000
        )

    # ---------------- DELETE TASK ----------------

    def delete_task(self):

        if self.selected_task_id is None:
            QMessageBox.information(
                self, "Select Task",
                "Please select a task to delete."
            )
            return

        reply = QMessageBox.question(
            self,
            "Confirm Deletion",
            "Delete the selected task permanently?",
            QMessageBox.StandardButton.Yes |
            QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No
        )

        if reply != QMessageBox.StandardButton.Yes:
            return

        try:
            self.repo.delete(self.selected_task_id)

        except Exception as error:
            self.show_database_error(error)
            return

        self.clear_form()
        self.refresh_tasks()

        self.statusBar().showMessage(
            "Task deleted successfully!", 5000
        )

    # ---------------- TOGGLE COMPLETION ----------------

    def toggle_completed(self):

        if self.selected_task_id is None:
            QMessageBox.information(
                self, "Select Task",
                "Please select a task first."
            )
            return

        try:
            self.repo.set_completed(
                self.selected_task_id,
                not self.completed_input.isChecked()
            )

        except Exception as error:
            self.show_database_error(error)
            return

        self.clear_form()
        self.refresh_tasks()

        self.statusBar().showMessage(
            "Task completion updated!", 5000
        )

    # ---------------- LOAD SELECTED TASK ----------------

    def load_selected_task(self):

        row = self.table.currentRow()

        if row < 0 or self.table.item(row, 0) is None:
            return

        task_id = int(self.table.item(row, 0).text())

        try:
            task = next(
                (
                    t for t in self.repo.all()
                    if t["id"] == task_id
                ),
                None
            )

        except Exception as error:
            self.show_database_error(error)
            return

        if task is None:
            return

        self.selected_task_id = task_id

        self.title_input.setText(task["title"])

        self.description_input.setPlainText(
            task["description"]
        )

        self.priority_input.setCurrentText(
            task["priority"]
        )

        self.date_input.setDate(
            QDate.fromString(
                task["due_date"], "yyyy-MM-dd"
            )
        )

        self.completed_input.setChecked(
            bool(task["completed"])
        )

    # ---------------- REFRESH TASK TABLE ----------------

    def refresh_tasks(self, *_):

        try:
            tasks = self.repo.all(
                self.search_input.text(),
                self.filter_priority.currentText(),
                self.filter_status.currentText()
            )

            total, done = self.repo.totals()

        except Exception as error:
            self.show_database_error(error)
            return

        self.table.blockSignals(True)

        try:
            self.table.setRowCount(len(tasks))

            for row, task in enumerate(tasks):

                values = (
                    task["id"],
                    task["title"],
                    task["priority"],
                    task["due_date"],
                    "Completed" if task["completed"] else "Pending"
                )

                for col, value in enumerate(values):

                    item = QTableWidgetItem(str(value))

                    if col == 2:
                        color = {
                            "High": "#ff8585",
                            "Medium": "#ffd166",
                            "Low": "#75d9b5"
                        }.get(task["priority"], "#ffffff")

                        item.setForeground(QColor(color))

                    self.table.setItem(row, col, item)

            self.table.clearSelection()

        finally:
            self.table.blockSignals(False)

        self.selected_task_id = None

        self.summary_label.setText(
            f"Total: {total} | Completed: {done} | "
            f"Pending: {total - done}"
        )

        percentage = (
            round(done / total * 100) if total else 0
        )

        self.progress.setValue(percentage)

    # ---------------- CLEAR FORM ----------------

    def clear_form(self):

        self.selected_task_id = None
        self.table.clearSelection()

        self.title_input.clear()
        self.description_input.clear()

        self.priority_input.setCurrentText("Medium")
        self.date_input.setDate(QDate.currentDate())
        self.completed_input.setChecked(False)

    # ---------------- PROGRESS CHART ----------------

    def show_progress_chart(self):

        try:
            total, done = self.repo.totals()

        except Exception as error:
            self.show_database_error(error)
            return

        pending = total - done

        dialog = QDialog(self)
        dialog.setWindowTitle(
            "Progress Chart | Yuepel | 08230241"
        )
        dialog.resize(460, 280)

        layout = QVBoxLayout(dialog)

        title = QLabel("TASK COMPLETION CHART")
        title.setStyleSheet(
            "font-size: 19px; font-weight: bold; "
            "color: #60a5fa;"
        )

        layout.addWidget(title)

        layout.addWidget(
            QLabel(f"Total Tasks: {total}")
        )

        layout.addWidget(
            QLabel(f"Completed: {done}")
        )

        completed_bar = QProgressBar()
        completed_bar.setRange(0, max(total, 1))
        completed_bar.setValue(done)
        completed_bar.setFormat(
            f"{done} completed"
        )

        layout.addWidget(completed_bar)

        layout.addWidget(
            QLabel(f"Pending: {pending}")
        )

        pending_bar = QProgressBar()
        pending_bar.setRange(0, max(total, 1))
        pending_bar.setValue(pending)
        pending_bar.setFormat(
            f"{pending} pending"
        )

        pending_bar.setStyleSheet(
            "QProgressBar::chunk { "
            "background: #f59e0b; }"
        )

        layout.addWidget(pending_bar)

        completion_rate = (
            round(done / total * 100) if total else 0
        )

        layout.addWidget(
            QLabel(f"Completion rate: {completion_rate}%")
        )

        close_button = QPushButton("Close")
        close_button.clicked.connect(dialog.accept)

        layout.addWidget(close_button)
        dialog.exec()

    # ---------------- DATABASE ERROR HANDLING ----------------

    def show_database_error(self, error):

        QMessageBox.critical(
            self,
            "Database Error",
            f"Unable to access task data.\n\nDetails: {error}"
        )

    # ---------------- ABOUT DIALOG ----------------

    def show_about(self):

        QMessageBox.about(
            self,
            "About Smart Student Task Manager",
            "Smart Student Task Manager\n\n"
            "Developed by: Yuepel\n"
            "Student ID: 08230241\n"
            "Framework: PyQt6\n"
            "Database: SQLite\n"
            "Unit V - Exploring GUI Frameworks"
        )
