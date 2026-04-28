from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QPushButton,
    QTableWidget, QTableWidgetItem, QMessageBox,
    QLineEdit, QHBoxLayout, QHeaderView
)
from database import get_books, insert_book, update_book, delete_book
from dialog_form import BookDialog


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("📚 Manajemen Buku Digital")

        self.widget = QWidget()
        self.layout = QVBoxLayout()

        # 🔍 SEARCH
        self.search = QLineEdit()
        self.search.setPlaceholderText("🔍 Cari buku...")
        self.search.setMinimumHeight(40)
        self.layout.addWidget(self.search)

        # 📊 TABLE
        self.table = QTableWidget()
        self.table.setColumnCount(6)
        self.table.setHorizontalHeaderLabels(
            ["ID", "Judul", "Penulis", "Tahun", "Genre", "Penerbit"]
        )
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.setAlternatingRowColors(True)
        self.layout.addWidget(self.table)

        # 🔘 BUTTON AREA (LEBIH KEREN)
        btn_layout = QHBoxLayout()

        self.btn_add = QPushButton("➕ Tambah")
        self.btn_edit = QPushButton("✏️ Edit")
        self.btn_delete = QPushButton("🗑 Hapus")

        btn_layout.addWidget(self.btn_add)
        btn_layout.addWidget(self.btn_edit)
        btn_layout.addWidget(self.btn_delete)

        self.layout.addLayout(btn_layout)

        self.widget.setLayout(self.layout)
        self.setCentralWidget(self.widget)

        # EVENT
        self.btn_add.clicked.connect(self.open_add)
        self.btn_edit.clicked.connect(self.open_edit)
        self.btn_delete.clicked.connect(self.delete_data)
        self.search.textChanged.connect(self.search_data)

        self.load_data()
        self.create_menu()

    # ================= MENU =================
    def create_menu(self):
        menu = self.menuBar()
        help_menu = menu.addMenu("Help")
        help_menu.addAction("Tentang Aplikasi", self.about)

    def about(self):
        QMessageBox.information(self, "About", "📚 Book Manager v1.0")

    # ================= LOAD =================
    def load_data(self):
        self.all_data = get_books()
        self.show_data(self.all_data)

    def show_data(self, data):
        self.table.setRowCount(len(data))
        for row_idx, row_data in enumerate(data):
            for col_idx, value in enumerate(row_data):
                self.table.setItem(
                    row_idx, col_idx, QTableWidgetItem(str(value))
                )

    # ================= CREATE =================
    def open_add(self):
        dialog = BookDialog()
        dialog.btn.clicked.connect(lambda: self.save_add(dialog))
        dialog.exec()

    def save_add(self, dialog):
        data = (
            dialog.title.text(),
            dialog.author.text(),
            dialog.year.text(),
            dialog.genre.text(),
            dialog.publisher.text()
        )

        if "" in data:
            QMessageBox.warning(self, "Error", "Semua field harus diisi!")
            return

        insert_book(data)
        dialog.close()
        self.load_data()

    # ================= UPDATE =================
    def open_edit(self):
        row = self.table.currentRow()
        if row == -1:
            QMessageBox.warning(self, "Error", "Pilih data dulu!")
            return

        data = [self.table.item(row, col).text() for col in range(6)]
        dialog = BookDialog(data)
        dialog.btn.clicked.connect(lambda: self.save_edit(dialog, data[0]))
        dialog.exec()

    def save_edit(self, dialog, book_id):
        new_data = (
            dialog.title.text(),
            dialog.author.text(),
            dialog.year.text(),
            dialog.genre.text(),
            dialog.publisher.text()
        )

        update_book(book_id, new_data)
        dialog.close()
        self.load_data()

    # ================= DELETE =================
    def delete_data(self):
        row = self.table.currentRow()
        if row == -1:
            QMessageBox.warning(self, "Error", "Pilih data dulu!")
            return

        book_id = self.table.item(row, 0).text()

        confirm = QMessageBox.question(
            self,
            "Konfirmasi",
            "Yakin mau hapus data ini?",
            QMessageBox.Yes | QMessageBox.No
        )

        if confirm == QMessageBox.Yes:
            delete_book(book_id)
            self.load_data()

    # ================= SEARCH =================
    def search_data(self):
        keyword = self.search.text().lower()
        filtered = []

        for row in self.all_data:
            if any(keyword in str(item).lower() for item in row):
                filtered.append(row)

        self.show_data(filtered)