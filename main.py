import sys
from PySide6.QtWidgets import QApplication
from main_window import MainWindow
from database import create_table

app = QApplication(sys.argv)

# Load QSS
with open("style.qss", "r") as f:
    app.setStyleSheet(f.read())

create_table()

window = MainWindow()
window.show()

sys.exit(app.exec())