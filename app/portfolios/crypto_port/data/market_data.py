import ccxt
import sqlite3
import pandas as pd
from database import DB_PATH

def get_last_timestamp():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("SELECT MAX(timestamp) FROM btc_daily")
    result = cursor.fetchone()[0]

    conn.close()
    return result


def update_market_data():

    exchange = ccxt.binance()
    last_ts = get_last_timestamp()

    since = last_ts if last_ts else None

    ohlcv = exchange.fetch_ohlcv(
        "BTC/USDT",
        timeframe="1d",
        since=since,
        limit=200
    )

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    for row in ohlcv:
        cursor.execute("""
        INSERT OR IGNORE INTO btc_daily
        VALUES (?, ?, ?, ?, ?, ?)
        """, tuple(row))

    conn.commit()
    conn.close()
