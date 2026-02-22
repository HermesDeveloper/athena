import sqlite3
import os
from config.settings import TREND_DB_PATH

def init_db():
    os.makedirs(os.path.dirname(TREND_DB_PATH), exist_ok=True)

    conn = sqlite3.connect(TREND_DB_PATH)
    c = conn.cursor()

    # log message
    c.execute("""
    CREATE TABLE IF NOT EXISTS logs(
        time TEXT,
        message TEXT
    )
    """)

    # market snapshot
    c.execute("""
    CREATE TABLE IF NOT EXISTS market_snapshot(
        time TEXT,
        market_state TEXT,
        exposure REAL,
        equity REAL
    )
    """)

    # order log
    c.execute("""
    CREATE TABLE IF NOT EXISTS order_log(
        time TEXT,
        symbol TEXT,
        side TEXT,
        qty INTEGER,
        price REAL
    )
    """)

    conn.commit()
    conn.close()
