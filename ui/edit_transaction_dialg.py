from PySide6.QtWidgets import QDialog, QVBoxLayout, QLabel, QLineEdit, QPushButton, QComboBox, QHBoxLayout, QMessageBox, QDateEdit
from PySide6.QtCore import QDate
from PySide6.QtGui import QDoubleValidator
from database.database import Database
class EditTransactionDialog(QDialog):
    def __init__(self, parent=None, transaction_id=None):
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
        self.amount_input.setValidator(QDoubleValidator(0.0, 1e9, 2))
        layout.addWidget(self.amount_input)
        layout.addWidget(QLabel("Category"))
        self.category_input = QLineEdit()
        layout.addWidget(self.category_input)
        layout.addWidget(QLabel("Subcategory"))
        self.subcategory_input = QLineEdit()
        layout.addWidget(self.subcategory_input)
        layout.addWidget(QLabel("Description"))
        self.desc_input = QLineEdit()
        layout.addWidget(self.desc_input)
        layout.addWidget(QLabel("Date"))
        self.date_input = QDateEdit()
        self.date_input.setDisplayFormat("yyyy-MM-dd")
        self.date_input.setCalendarPopup(True)
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
        if self.transaction_id is None:
            return
        trans = self.db.get_transaction_by_id(self.transaction_id)
        if not trans:
            return
        self.type_combo.setCurrentText(trans.type.capitalize())
        self.amount_input.setText(str(trans.amount))
        self.category_input.setText(trans.category or "")
        self.subcategory_input.setText(getattr(trans, "subcategory", "") or "")
        self.desc_input.setText(trans.description or "")
        try:
            y,m,d = map(int, trans.date.split('-'))
            self.date_input.setDate(QDate(y,m,d))
        except Exception:
            self.date_input.setDate(QDate.currentDate())
    def save_transaction(self):
        try:
            amount_text = self.amount_input.text().strip()
            if not amount_text:
                QMessageBox.warning(self,"Invalid Input", "Amount is required.")
                return
            amount = float(amount_text)
            date_str = self.date_input.date().toString("yyyy-MM-dd")
            subcategory = self.subcategory_input.text().strip() or None
            updated = self.db.update_transaction(
            self.transaction_id,
            self.type_combo.currentText(),
            amount,
            self.category_input.text().strip(),
            subcategory,
            self.desc_input.text().strip(),
            date_str
            )
            if updated == 0:
                QMessageBox.warning(self, "Error", "No transaction was updated. It may have been deleted.")
            else:
                QMessageBox.information(self, "Success", "Transaction updated successfully.")
                self.accept()
        except Exception as e:
            QMessageBox.warning(self, "Error", str(e))