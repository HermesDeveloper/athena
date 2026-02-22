import sqlite3
import pandas as pd
from config.settings import CRYPTO_DB_PATH

MAX = 0.80
MIN = 0.10
STEP = 0.10


def calc_target_weight(current_weight):

    conn = sqlite3.connect(CRYPTO_DB_PATH)

    df = pd.read_sql(
        "SELECT close FROM btc_daily ORDER BY timestamp DESC LIMIT 5",
        conn
    )

    conn.close()

    if len(df) < 3:
        print("Not enough data for momentum")
        return current_weight

    last = df.iloc[0]["close"]
    prev = df.iloc[2]["close"]

    change = (last - prev) / prev

    print("Momentum change:", round(change * 100, 2), "%")

    if change > 0.015:
        return min(MAX, current_weight + STEP)

    if change < -0.015:
        return max(MIN, current_weight - STEP)

    return current_weight