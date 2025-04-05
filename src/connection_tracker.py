import sqlite3
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

class ConnectionTracker:
    def __init__(self, db_path="data/connections.db"):
        self.db_path = db_path
        self._init_db()

    def _init_db(self):
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS connections (
                    profile_id TEXT PRIMARY KEY,
                    name TEXT,
                    sent_date TIMESTAMP,
                    status TEXT,
                    response_date TIMESTAMP,
                    company TEXT,
                    notes TEXT
                )
            """)

    def add_connection(self, profile_id, name, company, notes=""):
        try:
            with sqlite3.connect(self.db_path) as conn:
                conn.execute(
                    "INSERT INTO connections (profile_id, name, sent_date, status, company, notes) VALUES (?, ?, ?, ?, ?, ?)",
                    (profile_id, name, datetime.now(), "SENT", company, notes)
                )
            return True
        except sqlite3.IntegrityError:
            logger.warning(f"Connection request to {name} already exists")
            return False

    def update_status(self, profile_id, status):
        with sqlite3.connect(self.db_path) as conn:
            conn.execute(
                "UPDATE connections SET status = ?, response_date = ? WHERE profile_id = ?",
                (status, datetime.now(), profile_id)
            )

    def is_duplicate(self, profile_id):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute("SELECT COUNT(*) FROM connections WHERE profile_id = ?", (profile_id,))
            return cursor.fetchone()[0] > 0

    def get_connection_stats(self):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute("""
                SELECT status, COUNT(*) 
                FROM connections 
                GROUP BY status
            """)
            return dict(cursor.fetchall())
