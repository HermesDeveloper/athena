import sqlite3
import pandas as pd
from config.settings import CRYPTO_DB_PATH

INITIAL = 100000

state = {
    "value": INITIAL,
    "btc_weight": 0.5
}

def update_portfolio(new_weight):
    conn = sqlite3.connect(CRYPTO_DB_PATH)

    price_df = pd.read_sql(
        "SELECT close FROM btc_daily ORDER BY timestamp DESC LIMIT 1",
        conn
    )
    conn.close()

    if price_df.empty:
        return

    price = price_df.iloc[0]["close"]

    state["btc_weight"] = new_weight

    btc_value = state["value"] * new_weight
    cash = state["value"] - btc_value

    print("\n====== PORT ======")
    print("BTC price:", round(price,2))
    print("BTC weight:", round(new_weight*100,1), "%")
    print("BTC value:", round(btc_value,2))
    print("Cash:", round(cash,2))
    print("Total:", round(state["value"],2))