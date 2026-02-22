import sqlite3
from datetime import datetime


from portfolios.trend_port.execution.alpaca_client import (
    get_account,
    get_positions,
    submit_market
)

from config.settings import (
    TREND_DB_PATH,
    DD_LEVEL_1,
    DD_LEVEL_2,
    DD_LEVEL_3,
    DD_LEVEL_4,
    REDUCE_L1,
    REDUCE_L2,
    REDUCE_L3,
    REDUCE_L4
)


# ======================================
# EQUITY PEAK STORAGE
# ======================================

def _ensure_peak_table():
    conn = sqlite3.connect(TREND_DB_PATH)
    c = conn.cursor()

    c.execute("""
    CREATE TABLE IF NOT EXISTS equity_peak(
        peak REAL
    )
    """)

    conn.commit()
    conn.close()


def get_peak_equity():
    _ensure_peak_table()

    conn = sqlite3.connect(TREND_DB_PATH)
    c = conn.cursor()

    c.execute("SELECT peak FROM equity_peak")
    row = c.fetchone()

    conn.close()

    if row is None:
        return None

    return float(row[0])


def update_peak_equity(equity):
    _ensure_peak_table()

    conn = sqlite3.connect(TREND_DB_PATH)
    c = conn.cursor()

    c.execute("DELETE FROM equity_peak")
    c.execute("INSERT INTO equity_peak VALUES (?)", (equity,))

    conn.commit()
    conn.close()


# ======================================
# PORTFOLIO DRAWDOWN CHECK (5 MIN)
# ======================================

def intraday_risk_check():

    account = get_account()
    equity = float(account.equity)

    peak = get_peak_equity()

    # ถ้ายังไม่มี peak หรือทำ new high
    if peak is None or equity > peak:
        update_peak_equity(equity)
        print("📈 New peak equity:", equity)
        return

    drawdown = (peak - equity) / peak

    print(f"🔎 Portfolio Drawdown: {drawdown:.2%}")

    reduce_ratio = None

    if drawdown >= DD_LEVEL_4:
        reduce_ratio = REDUCE_L4
    elif drawdown >= DD_LEVEL_3:
        reduce_ratio = REDUCE_L3
    elif drawdown >= DD_LEVEL_2:
        reduce_ratio = REDUCE_L2
    elif drawdown >= DD_LEVEL_1:
        reduce_ratio = REDUCE_L1

    if reduce_ratio is None:
        return

    print(f"⚠ Risk Triggered → Reduce {int(reduce_ratio * 100)}%")

    positions = get_positions()

    for p in positions:
        qty = int(float(p.qty))
        reduce_qty = int(qty * reduce_ratio)

        if reduce_qty > 0:
            submit_market(p.symbol, reduce_qty, "SELL")
