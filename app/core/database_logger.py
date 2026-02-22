import sqlite3
from datetime import datetime
from config.settings import TREND_DB_PATH


def log_market_snapshot(market_state, exposure, equity):

    conn = sqlite3.connect(TREND_DB_PATH)
    c = conn.cursor()

    c.execute("""
        INSERT INTO market_snapshot
        VALUES (?, ?, ?, ?)
    """, (
        datetime.now().isoformat(),
        market_state,
        exposure,
        equity
    ))

    conn.commit()
    conn.close()
