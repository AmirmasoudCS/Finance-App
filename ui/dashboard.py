from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QTableWidget, QTableWidgetItem, QHeaderView, QPushButton, QMessageBox, QFrame, QAbstractItemView
from PySide6.QtCore import Qt
from datetime import datetime
from database.database import Database
class DashboardPage(QWidget):
    def __init__(self):
        super().__init__()
        self.db = Database()
        self._setup_ui()
        self.refresh_dashboard()
    def _setup_ui(self):
        main_layout = QVBoxLayout()
        header_layout = QHBoxLayout()
        title_label = QLabel("Dashboard")
        title_label.setStyleSheet("font-size : 18px; font-weight : bold;")
        self.refresh_button = QPushButton("Refresh")
        self.refresh_button.clicked.connect(self.refresh_dashboard)
        header_layout.addWidget(title_label)
        header_layout.addStretch()
        header_layout.addWidget(self.refresh_button)
        main_layout.addLayout(header_layout)
        separator = QFrame()
        separator.setFrameShape(QFrame.Shape.HLine)
        separator.setFrameShadow(QFrame.Shadow.Sunken)
        main_layout.addWidget(separator)
        self.summary_title_label = QLabel("")
        self.summary_title_label.setStyleSheet("font-size : 14px; font-weight : bold;")
        main_layout.addWidget(self.summary_title_label)
        self.income_label = QLabel("Income: 0.00")
        self.expense_label = QLabel("Expenses: 0.00")
        self.balance_label = QLabel("Net Balance: 0.00")
        for label in (self.income_label, self.expense_label, self.balance_label):
            label.setAlignment(Qt.AlignmentFlag.AlignLeft)
            label.setStyleSheet("font-size : 13px; font-weight : bold;")
        main_layout.addWidget(self.income_label)
        main_layout.addWidget(self.expense_label)
        main_layout.addWidget(self.balance_label)
        main_layout.addSpacing(10)
        top_cat_title = QLabel("Top Expense Categories (This Month)")
        top_cat_title.setStyleSheet("font-size : 13px; font-weight : bold;")
        main_layout.addWidget(top_cat_title)
        self.top_categories_table = QTableWidget()
        self.top_categories_table.setColumnCount(2)
        self.top_categories_table.setHorizontalHeaderLabels(["Category", "Total Amount"])
        self.top_categories_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.top_categories_table.verticalHeader().setVisible(False)
        self.top_categories_table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.top_categories_table.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        main_layout.addWidget(self.top_categories_table)
        main_layout.addSpacing(10)
        recent_title = QLabel("Recent Transactions")
        recent_title.setStyleSheet("font-size : 13px; font-weight : bold;")
        main_layout.addWidget(recent_title)
        self.recent_table = QTableWidget()
        self.recent_table.setColumnCount(4)
        self.recent_table.setHorizontalHeaderLabels(["Date", "Type", "Category", "Amount"])
        self.recent_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.recent_table.verticalHeader().setVisible(False)
        self.recent_table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.recent_table.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        main_layout.addWidget(self.recent_table)
        self.setLayout(main_layout)
    def refresh_dashboard(self):
        try:
            now = datetime.now()
            year = str(now.year)
            month = f"{now.month:02d}"
            month_name = now.strftime("%B")
            self.summary_title_label.setText(f"Summary for {month_name} {year}")
            summary = self.db.get_month_summary(year,month)
            income = summary.get("income",0)
            expenses = summary.get("expense",0)
            balance = income - expenses
            self.income_label.setText(f"Income: {income:.2f}")
            self.expense_label.setText(f"Expenses: {expenses:.2f}")
            self.balance_label.setText(f"Net Balance: {balance:.2f}")
            cat_stats = self.db.get_category_stats(year, month)
            top_cats = sorted(cat_stats.items(), key = lambda x: x[1], reverse=True)[:3]
            self.top_categories_table.setRowCount(len(top_cats))
            for row_idx, (category, total) in enumerate(top_cats):
                self.top_categories_table.setItem(row_idx, 0, QTableWidgetItem(category))
                self.top_categories_table.setItem(row_idx, 1, QTableWidgetItem(f"{total:.2f}"))
            all_transactions = self.db.get_all_transactions()
            recent = sorted(all_transactions, key = lambda t: t.date, reverse=True)[:5]
            self.recent_table.setRowCount(len(recent))
            for row_idx,trans in enumerate(recent):
                self.recent_table.setItem(row_idx, 0, QTableWidgetItem(str(trans.date)))
                self.recent_table.setItem(row_idx, 1, QTableWidgetItem(trans.type))
                self.recent_table.setItem(row_idx, 2, QTableWidgetItem(trans.category))
                self.recent_table.setItem(row_idx, 3, QTableWidgetItem(f"{trans.amount:.2f}"))
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to load dashboard.\n{e}")

