import requests
import sqlite3
from config.settings import CRYPTO_DB_PATH

URL = "https://api.binance.com/api/v3/klines"

def fetch_and_store():
    params = {
        "symbol": "BTCUSDT",
        "interval": "5m",
        "limit": 100
    }

    data = requests.get(URL, params=params).json()

    conn = sqlite3.connect(CRYPTO_DB_PATH)

    for k in data:
        ts = int(k[0] / 1000)

        conn.execute("""
        INSERT OR REPLACE INTO btc_daily
        VALUES (?, ?, ?, ?, ?, ?)
        """, (
            ts,
            float(k[1]),
            float(k[2]),
            float(k[3]),
            float(k[4]),
            float(k[5])
        ))

    conn.commit()
    conn.close()

    print("BTC updated from Binance")