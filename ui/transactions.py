from PySide6.QtWidgets import QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem, QHeaderView
from database.database import Database
class TransactionsPage(QWidget):
    def __init__(self):
        super().__init__()
        self.db = Database()
        layout = QVBoxLayout()
        self.table = QTableWidget()
        self.table.setSortingEnabled(True)
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        layout.addWidget(self.table)
        self.setLayout(layout)
        self.load_transactions()
    def load_transactions(self):
        transactions = self.db.get_all_transactions()
        self.table.setRowCount(len(transactions))
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(["Type", "Amount", "Category", "Description", "Date"])
        for row_idx, trans in enumerate(transactions):
            self.table.setItem(row_idx, 0, QTableWidgetItem(trans.type))
            self.table.setItem(row_idx, 1, QTableWidgetItem(str(trans.amount)))
            self.table.setItem(row_idx, 2, QTableWidgetItem(trans.category))
            self.table.setItem(row_idx, 3, QTableWidgetItem(trans.description))
            self.table.setItem(row_idx, 4, QTableWidgetItem(trans.date))
    