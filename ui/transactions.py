from PySide6.QtWidgets import QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem, QHeaderView, QMenu, QMessageBox
from database.database import Database
from PySide6.QtCore import Qt, QPoint
from ui.edit_transaction_dialg import EditTransactionDialog

class TransactionsPage(QWidget):
    def __init__(self):
        super().__init__()
        self.db = Database()
        layout = QVBoxLayout()
        self.table = QTableWidget()
        self.table.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.table.customContextMenuRequested.connect(self.open_menu)
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
            type_item = QTableWidgetItem(trans.type)
            type_item.setData(Qt.ItemDataRole.UserRole, trans.id)
            self.table.setItem(row_idx, 0, type_item)
            self.table.setItem(row_idx, 1, QTableWidgetItem(str(trans.amount)))
            self.table.setItem(row_idx, 2, QTableWidgetItem(trans.category))
            self.table.setItem(row_idx, 3, QTableWidgetItem(trans.description))
            self.table.setItem(row_idx, 4, QTableWidgetItem(trans.date))
    def open_menu(self, pos:QPoint):
        item = self.table.itemAt(pos)
        if item is None:
            return
        row = item.row()
        id_item = self.table.item(row, 0)
        if id_item is None:
            return
        transaction_id = id_item.data(Qt.ItemDataRole.UserRole)
        menu = QMenu(self)
        edit_action = menu.addAction("Edit")
        delete_action = menu.addAction("Delete")
        action = menu.exec(self.table.viewport().mapToGlobal(pos))
        if action == delete_action:
            self.delete_transaction(transaction_id)
        if action == edit_action:
            self.open_edit_dialog(transaction_id)
    def delete_transaction(self, transaction_id):
        confirm = QMessageBox.question(self, "Delete Transaction", "Are you sure you want to delete this transaction?", QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        if confirm == QMessageBox.StandardButton.Yes:
            self.db.delete_transaction(transaction_id)
            self.load_transactions()
    def open_edit_dialog(self, transaction_id):
        dialog = EditTransactionDialog(self, transaction_id)
        if dialog.exec():
            self.load_transactions()
