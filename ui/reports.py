from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QComboBox, QTableWidget, QTableWidgetItem, QMessageBox, QHeaderView
from PySide6.QtCore import Qt
from datetime import datetime
from database.database import Database
class ReportsPage(QWidget):
    def __init__(self):
        super().__init__()
        self.db = Database()
        self._setup_ui()
    def _setup_ui(self):
        main_layout = QVBoxLayout()
        date_layout = QHBoxLayout()
        current_year = datetime.now().year
        current_month = datetime.now().month
        self.year_combo = QComboBox()
        for y in range(current_year - 5, current_year + 1):
            self.year_combo.addItem(str(y))
        self.year_combo.setCurrentText(str(current_year))
        self.month_combo = QComboBox()
        self.month_combo.addItems(["01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11", "12"])
        self.month_combo.setCurrentText(f"{current_month:02d}")
        self.generate_button = QPushButton("Generate Report")
        self.generate_button.clicked.connect(self.generate_report)

        date_layout.addWidget(QLabel("Year:"))
        date_layout.addWidget(self.year_combo)
        date_layout.addWidget(QLabel("Month:"))
        date_layout.addWidget(self.month_combo)
        date_layout.addWidget(self.generate_button)
        main_layout.addLayout(date_layout)

        self.income_label = QLabel("Income: 0.00")
        self.expense_label = QLabel("Expense: 0.00")
        self.balance_label = QLabel("Net Balance: 0.00")
        for label in (self.income_label, self.expense_label, self.balance_label):
            label.setAlignment(Qt.AlignmentFlag.AlignLeft)
            label.setStyleSheet("font-size : 14px; font-weight : bold")
        main_layout.addWidget(self.income_label)
        main_layout.addWidget(self.expense_label)
        main_layout.addWidget(self.balance_label)

        self.category_table = QTableWidget()
        self.category_table.setColumnCount(2)
        self.category_table.setHorizontalHeaderLabels(["Category", "Total Amount"])
        self.category_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.category_table.verticalHeader().setVisible(False)
        main_layout.addWidget(QLabel("Category Breakdown"))
        main_layout.addWidget(self.category_table)
        self.setLayout(main_layout)
    def generate_report(self):
        year = self.year_combo.currentText()
        month = self.month_combo.currentText()
        try:
            summary = self.db.get_month_summary(year, month)
            cat_stats = self.db.get_category_stats(year, month)
            income = summary.get("income", 0)
            expense = summary.get("expense", 0)
            balance = income - expense
            self.income_label.setText(f"Income: {income:.2f}")
            self.expense_label.setText(f"Expenses: {expense:.2f}")
            self.balance_label.setText(f"Net Balance: {balance:.2f}")
            self.category_table.setRowCount(len(cat_stats))
            for row_idx,row in enumerate(cat_stats):
                self.category_table.setItem(row_idx, 0, QTableWidgetItem(row["category"]))
                self.category_table.setItem(row_idx, 1, QTableWidgetItem(f"{row['total']:.2f}"))
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to load report:\n{e}")

