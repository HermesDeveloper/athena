import sqlite3
from config.settings import CRYPTO_DB_PATH


def get_conn():
    return sqlite3.connect(CRYPTO_DB_PATH)


def init_crypto_db():
    with get_conn() as conn:
        cursor = conn.cursor()

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS btc_daily (
            timestamp INTEGER PRIMARY KEY,
            open REAL,
            high REAL,
            low REAL,
            close REAL,
            volume REAL
        )
        """)