"""Entry point for the Smart Student Task Manager."""
import sys
from PyQt6.QtWidgets import QApplication
from database import TaskRepository
from ui import TaskManagerWindow


def main():
    app = QApplication(sys.argv)
    window = TaskManagerWindow(TaskRepository())
    window.show()
    return app.exec()


if __name__ == "__main__":
    sys.exit(main())
