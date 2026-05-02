from PySide6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QPushButton, QStackedWidget
from ui.add_transactions import AddTransactionPage
from ui.transactions import TransactionsPage
from ui.reports import ReportsPage
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Finance Manager")
        self.resize(900,600)
        container = QWidget()
        self.setCentralWidget(container)
        
        layout = QVBoxLayout(container)
        
        self.btn_add = QPushButton("Add Transaction")
        self.btn_view = QPushButton("View Transactions")
        self.btn_reports = QPushButton("Reports")
        
        self.stack = QStackedWidget()
        layout.addWidget(self.btn_add)
        layout.addWidget(self.btn_view)
        layout.addWidget(self.btn_reports)
        layout.addWidget(self.stack)

        self.page_add = AddTransactionPage()
        self.page_view = TransactionsPage()
        self.page_reports = ReportsPage()

        self.stack.addWidget(self.page_add)
        self.stack.addWidget(self.page_view)
        self.stack.addWidget(self.page_reports)

        self.btn_add.clicked.connect(lambda : self.stack.setCurrentWidget(self.page_add))
        self.btn_view.clicked.connect(lambda : self.stack.setCurrentWidget(self.page_view))
        self.btn_reports.clicked.connect(lambda : self.stack.setCurrentWidget(self.page_reports))
        