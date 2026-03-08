import sqlite3
import pandas as pd
import time
from datetime import datetime

from portfolios.crypto_port.trading.regime import get_regime
from portfolios.crypto_port.trading.momentum_engine import calc_target_weight

from portfolios.crypto_port.portfolio.allocator import (
    calculate_portfolio_value,
    get_btc_weight
)

from portfolios.crypto_port.risk.risk_engine import check_drawdown

from portfolios.crypto_port.trading.execution import (
    get_balance,
    buy_btc,
    sell_btc
)

from portfolios.crypto_port.data.database import init_crypto_db
from config.settings import CRYPTO_DB_PATH


# ===== GLOBAL STATE =====

INITIAL_CAPITAL = None
peak_equity = None

LAST_TRADE_TIME = None
LAST_DECISION_TIME = None


# ===== TIMERS =====

MIN_TRADE_INTERVAL = 60 * 60 * 6   # 6 hours
CHECK_INTERVAL = 300               # 5 minutes
TRADE_INTERVAL = 1800              # 30 minutes


# ===== PRICE FETCH =====

def get_latest_price():

    conn = sqlite3.connect(CRYPTO_DB_PATH)

    df = pd.read_sql(
        "SELECT close FROM btc_daily ORDER BY timestamp DESC LIMIT 1",
        conn
    )

    conn.close()

    if df.empty:
        return None

    return df.iloc[0]["close"]


# ===== MAIN CYCLE =====

def run_cycle():

    global peak_equity
    global INITIAL_CAPITAL
    global LAST_TRADE_TIME
    global LAST_DECISION_TIME

    init_crypto_db()

    btc_price = get_latest_price()

    if btc_price is None:
        print("No BTC price data yet")
        return

    btc_balance, cash = get_balance()

    # ===== INITIAL PORTFOLIO SETUP =====

    if btc_balance == 0 and cash > 0:

        init_buy = cash * 0.5

        if init_buy >= 10:
            print("\nPortfolio initialized")
            buy_btc(init_buy)

        btc_balance, cash = get_balance()

    core_btc = btc_balance
    trading_btc = 0

    # ===== REGIME =====

    regime = get_regime()

    # ===== PORTFOLIO VALUE =====

    total_equity = calculate_portfolio_value(
        btc_price,
        core_btc,
        trading_btc,
        cash
    )

    if total_equity == 0:
        return

    if INITIAL_CAPITAL is None:
        INITIAL_CAPITAL = total_equity

    pnl = total_equity - INITIAL_CAPITAL
    pnl_pct = (pnl / INITIAL_CAPITAL) * 100

    # ===== PEAK TRACK =====

    if peak_equity is None:
        peak_equity = total_equity

    if total_equity > peak_equity:
        peak_equity = total_equity

    risk_trigger, dd = check_drawdown(total_equity, peak_equity)

    # ===== MOMENTUM =====

    current_weight = get_btc_weight(
        btc_price,
        core_btc,
        trading_btc,
        cash
    )

    target_weight = calc_target_weight(current_weight)

    btc_amount = core_btc + trading_btc
    btc_value = btc_amount * btc_price

    btc_weight_pct = (btc_value / total_equity) * 100
    target_pct = target_weight * 100

    diff_pct = target_pct - btc_weight_pct

    # ===== STATUS =====

    print("\n===================================")
    print("Time:", datetime.now())
    print("===================================")

    print(f"BTC price : {btc_price:.2f}")
    print(f"Regime    : {regime}")

    print("\nPortfolio")
    print(f"Equity : {total_equity:.2f}")
    print(f"PnL    : {pnl:.2f} ({pnl_pct:.2f}%)")

    print("\nHoldings")
    print(f"BTC  : {btc_amount:.5f}")
    print(f"Cash : {cash:.2f}")

    print("\nAllocation")
    print(f"BTC weight : {btc_weight_pct:.2f}%")
    print(f"Target     : {target_pct:.2f}%")

    print("\nRisk")
    print(f"Drawdown : {dd:.4f}")
    print(f"Trigger  : {risk_trigger}")

    # ===== TRADE WINDOW CHECK (30 min) =====

    now = time.time()

    if LAST_DECISION_TIME is not None:
        if now - LAST_DECISION_TIME < TRADE_INTERVAL:
            print("\nSignal checked (waiting for trade window)")
            return

    LAST_DECISION_TIME = now

    # ===== REBALANCE CHECK =====

    threshold = 2

    if abs(diff_pct) < threshold:
        print("\nSkip rebalance (diff < 2%)")
        return

    # ===== TRADE COOLDOWN (6 hours) =====

    if LAST_TRADE_TIME is not None:

        if now - LAST_TRADE_TIME < MIN_TRADE_INTERVAL:
            print("\nTrade cooldown active")
            return

    # ===== EXECUTE TRADE =====

    if diff_pct > 0:

        buy_value = total_equity * (diff_pct / 100)

        if buy_value < 10:
            print("\nBuy too small")
            return

        print(f"\nBUY ${buy_value:.2f} BTC")
        buy_btc(buy_value)

    else:

        sell_value = total_equity * (abs(diff_pct) / 100)

        if sell_value < 10:
            print("\nSell too small")
            return

        qty = sell_value / btc_price

        print(f"\nSELL {qty:.6f} BTC")
        sell_btc(qty)

    LAST_TRADE_TIME = time.time()


# ===== BOT LOOP =====

def run_bot():

    print("\nCrypto Trading Bot Started\n")

    while True:

        try:

            run_cycle()

            print("\nNext update in 5 minutes...\n")

            time.sleep(CHECK_INTERVAL)

        except Exception as e:

            print("Bot error:", e)

            time.sleep(60)


# ===== START BOT =====

if __name__ == "__main__":

    run_bot()