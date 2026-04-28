from PySide6.QtWidgets import QDialog, QFormLayout, QLineEdit, QPushButton


class BookDialog(QDialog):
    def __init__(self, data=None):
        super().__init__()
        self.setWindowTitle("Form Buku")

        layout = QFormLayout()

        self.title = QLineEdit()
        self.author = QLineEdit()
        self.year = QLineEdit()
        self.genre = QLineEdit()
        self.publisher = QLineEdit()

        # 🔥 kalau edit → isi otomatis
        if data:
            self.title.setText(data[1])
            self.author.setText(data[2])
            self.year.setText(data[3])
            self.genre.setText(data[4])
            self.publisher.setText(data[5])

        layout.addRow("Judul", self.title)
        layout.addRow("Penulis", self.author)
        layout.addRow("Tahun", self.year)
        layout.addRow("Genre", self.genre)
        layout.addRow("Penerbit", self.publisher)

        self.btn = QPushButton("Simpan")
        layout.addWidget(self.btn)

        self.setLayout(layout)