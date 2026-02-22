import sqlite3
import pandas as pd

from portfolios.crypto_port.config import FAST_MA, SLOW_MA
from config.settings import CRYPTO_DB_PATH


def get_regime():
    conn = sqlite3.connect(CRYPTO_DB_PATH)
    df = pd.read_sql("SELECT * FROM btc_daily ORDER BY timestamp", conn)
    conn.close()

    # ❗ ไม่มีข้อมูลเลย
    if df.empty:
        print("⚠️ btc_daily empty → default BEAR")
        return "BEAR"

    df["fast"] = df["close"].rolling(FAST_MA).mean()
    df["slow"] = df["close"].rolling(SLOW_MA).mean()

    # ❗ ข้อมูลยังไม่พอคำนวณ MA
    if pd.isna(df["fast"].iloc[-1]) or pd.isna(df["slow"].iloc[-1]):
        print("⚠️ not enough candles for MA → BEAR")
        return "BEAR"

    if df["fast"].iloc[-1] > df["slow"].iloc[-1]:
        return "BULL"

    return "BEAR"