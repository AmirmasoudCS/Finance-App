from PySide6.QtWidgets import QWidget, QVBoxLayout, QFormLayout, QLineEdit, QComboBox, QPushButton, QDateEdit, QMessageBox
from PySide6.QtCore import QDate
from database.database import Database
from logic.categorizer import auto_category
class AddTransactionPage(QWidget):
    def __init__(self):
        super().__init__()
        self.db = Database()
        
        layout = QVBoxLayout()
        form = QFormLayout()

        self.type_box = QComboBox()
        self.type_box.addItems(["Income","Expense"])
        form.addRow("Type:", self.type_box)

        self.amount_input = QLineEdit()
        self.amount_input.setPlaceholderText("Enter amount")
        form.addRow("Amount:",self.amount_input)

        self.desc_input = QLineEdit()
        self.desc_input.setPlaceholderText("e.g. Grocery store, salary, medicine ... ")
        form.addRow("Description",self.desc_input)

        self.category_input = QLineEdit()
        self.category_input.setPlaceholderText("Auto Category")
        self.category_input.setReadOnly(True)
        form.addRow("Category:",self.category_input)

        self.subcategory_input = QLineEdit()
        self.subcategory_input.setPlaceholderText("Optional Subcategory")
        form.addRow("Subcategory:", self.subcategory_input)


        self.date_input = QDateEdit()
        self.date_input.setCalendarPopup(True)
        self.date_input.setDate(QDate.currentDate())
        form.addRow("Date:",self.date_input)

        self.save_btn = QPushButton("Save Transaction")
        form.addRow(self.save_btn)
        
        layout.addLayout(form)
        self.setLayout(layout)

        self.desc_input.textChanged.connect(self.update_category)
        self.save_btn.clicked.connect(self.save_transaction)

    def update_category(self):
        desc = self.desc_input.text().strip()
        if desc:
            cat, subcat = auto_category(desc)
            self.category_input.setText(cat)
            if subcat:
                self.subcategory_input.setText(subcat)
            else:
                self.subcategory_input.clear()
        else:
            self.category_input.clear()
            self.subcategory_input.clear()
    
    def save_transaction(self):
        type_ = self.type_box.currentText().lower()
        amount_text = self.amount_input.text().strip()
        description = self.desc_input.text().strip()
        category = self.category_input.text().strip() or "Other"
        subcategory = self.subcategory_input.text().strip() or None
        date = self.date_input.date().toString("yyyy-MM-dd")
        if not amount_text or not description:
            QMessageBox.warning(self,"Input Error","Please fill in amount and description.")
            return
        try:
            amount = float(amount_text)
        except ValueError:
            QMessageBox.warning(self,"Input Error","Amount must be a valid number.")
            return
        try:
            self.db.add_transaction(type_, amount, category, subcategory, description, date)

            QMessageBox.information(self,"Success","Transaction saved successfully!")
            self.amount_input.clear()
            self.desc_input.clear()
            self.category_input.clear()
            self.subcategory_input.clear()
            self.date_input.setDate(QDate.currentDate())
        except Exception as e:
            QMessageBox.critical(self,"Database Error",f"Could not save transaction : {e}")


