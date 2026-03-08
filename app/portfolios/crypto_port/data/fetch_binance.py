import sqlite3
from portfolios.crypto_port.binance_client import get_client
from config.settings import CRYPTO_DB_PATH


def fetch_and_store():

    client = get_client()

    klines = client.get_klines(
        symbol="BTCUSDT",
        interval="1d",
        limit=1
    )

    candle = klines[0]

    timestamp = candle[0]
    close_price = float(candle[4])

    conn = sqlite3.connect(CRYPTO_DB_PATH)
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT OR IGNORE INTO btc_daily (timestamp, close)
        VALUES (?, ?)
        """,
        (timestamp, close_price)
    )

    conn.commit()
    conn.close()

    print("BTC updated from Binance")