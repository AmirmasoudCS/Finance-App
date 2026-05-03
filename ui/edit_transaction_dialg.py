from PySide6.QtWidgets import QDialog, QVBoxLayout, QLabel, QLineEdit, QPushButton, QComboBox, QHBoxLayout, QMessageBox
from database.database import Database
class EditTransactionDialog(QDialog):
    def __init__(self, transaction_id):
        super().__init__()
        self.db = Database()
        self.transaction_id = transaction_id
        self.setWindowTitle("Edit Transaction")
        self.setMinimumWidth(300)
        layout = QVBoxLayout()
        layout.addWidget(QLabel("Type"))
        self.type_combo = QComboBox()
        self.type_combo.addItems(["Income", "Expense"])
        layout.addWidget(self.type_combo)
        layout.addWidget(QLabel("Amount"))
        self.amount_input = QLineEdit()
        layout.addWidget(self.amount_input)
        layout.addWidget(QLabel("Category"))
        self.category_input = QLineEdit()
        layout.addWidget(self.category_input)
        layout.addWidget(QLabel("Description"))
        self.desc_input = QLineEdit()
        layout.addWidget(self.desc_input)
        layout.addWidget(QLabel("Date"))
        self.date_input = QLineEdit()
        layout.addWidget(self.date_input)

        btn_layout = QHBoxLayout()
        save_btn = QPushButton("Save")
        cancel_btn = QPushButton("Cancel")
        save_btn.clicked.connect(self.save_transaction)
        cancel_btn.clicked.connect(self.reject)
        btn_layout.addWidget(save_btn)
        btn_layout.addWidget(cancel_btn)
        layout.addLayout(btn_layout)
        self.setLayout(layout)
        self.load_transaction()
    def load_transaction(self):
        trans = self.db.get_transaction_by_id(self.transaction_id)
        if not trans:
            return
        self.type_combo.setCurrentText(trans.type)
        self.amount_input.setText(str(trans.amount))
        self.category_input.setText(trans.category)
        self.desc_input.setText(trans.description)
        self.date_input.setText(trans.date)
    def save_transaction(self):
        try:
            self.db.update_transaction(self.transaction_id, self.type_combo.currentText(), float(self.amount_input.text()), self.category_input.text(), self.desc_input.text(), self.date_input.text())
            self.accept()
        except Exception as e:
            QMessageBox.warning(self, "Error", f"{e}")