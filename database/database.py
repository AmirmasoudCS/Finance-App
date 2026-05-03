import sqlite3
from pathlib import Path
from database.models import Transaction


class Database:

    def __init__(self, db_name="finance.db"):
        base_dir = Path(__file__).resolve().parent.parent
        self.db_path = base_dir / db_name
        self.init_db()

    def _connect(self):
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn

    def init_db(self):
        query = """
        CREATE TABLE IF NOT EXISTS transactions(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            type TEXT NOT NULL,
            amount REAL NOT NULL,
            category TEXT NOT NULL,
            description TEXT,
            date TEXT NOT NULL
        )
        """

        with self._connect() as conn:
            conn.execute(query)

    def add_transaction(self, type_, amount, category, description, date):

        query = """
        INSERT INTO transactions(type, amount, category, description, date)
        VALUES(?, ?, ?, ?, ?)
        """

        with self._connect() as conn:
            conn.execute(query, (type_, amount, category, description, date))

    def get_all_transactions(self):

        query = """
        SELECT id, type, amount, category, description, date
        FROM transactions
        ORDER BY date DESC, id DESC
        """

        with self._connect() as conn:
            rows = conn.execute(query).fetchall()

        return [
            Transaction(
                id=row["id"],
                type=row["type"],
                amount=row["amount"],
                category=row["category"],
                description=row["description"],
                date=row["date"]
            )
            for row in rows
        ]

    def get_month_summary(self, year, month):

        month_str = f"{month:02d}"
        start_date = f"{year}-{month_str}-01"
        end_date = f"{year}-{month_str}-31"

        with self._connect() as conn:

            income = conn.execute(
                """
                SELECT COALESCE(SUM(amount),0)
                FROM transactions
                WHERE type='income' AND date BETWEEN ? AND ?
                """,
                (start_date, end_date)
            ).fetchone()[0]

            expense = conn.execute(
                """
                SELECT COALESCE(SUM(amount),0)
                FROM transactions
                WHERE type='expense' AND date BETWEEN ? AND ?
                """,
                (start_date, end_date)
            ).fetchone()[0]

        return {
            "income": income,
            "expense": expense,
            "balance": income - expense
        }

    def get_category_stats(self, year, month):

        month_str = f"{month:02d}"
        start_date = f"{year}-{month_str}-01"
        end_date = f"{year}-{month_str}-31"

        query = """
        SELECT category, SUM(amount)
        FROM transactions
        WHERE type='expense' AND date BETWEEN ? AND ?
        GROUP BY category
        ORDER BY SUM(amount) DESC
        """

        with self._connect() as conn:
            rows = conn.execute(query, (start_date, end_date)).fetchall()

        return {row["category"]: row["SUM(amount)"] for row in rows}
    def update_transaction(self, transaction_id, type_, amount, category, description, date):
        query = """
                UPDATE transactions SET type = ?, amount = ?, category = ?, description = ?, date = ? WHERE id = ?
                """
        with self._connect() as conn:
            conn.execute(query,(type_, amount, category, description, date, transaction_id))
    def delete_transaction(self, transaction_id):
        query = """
                DELETE FROM transactions WHERE id = ?
                """
        with self._connect() as conn:
            conn.execute(query,(transaction_id,))
    def get_transaction_by_id(self, transaction_id):
        query = """
                SELECT * FROM transactions WHERE id = ?
                """
        with self._connect() as conn:
            row = conn.execute(query, (transaction_id,)).fetchone()
            if row :
                return Transaction(
                    id=row['id'],
                    type=row['type'],
                    amount=row['amount'],
                    category=row['category'],
                    description=row['description'],
                    date=row['date']
                )
            return None