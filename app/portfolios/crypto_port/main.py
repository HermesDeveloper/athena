import sqlite3
import pandas as pd

from portfolios.crypto_port.trading.regime import get_regime
from portfolios.crypto_port.trading.strategy import trading_btc_weight_of_portfolio
from portfolios.crypto_port.core.core_holder import core_action
from portfolios.crypto_port.portfolio.allocator import calculate_portfolio_value
from portfolios.crypto_port.risk.risk_engine import check_drawdown
from portfolios.crypto_port.data.database import init_crypto_db
from portfolios.crypto_port.trading.momentum_engine import calc_target_weight
from portfolios.crypto_port.portfolio.allocator import get_btc_weight

from config.settings import CRYPTO_DB_PATH


# ===== MOCK PORTFOLIO STATE =====
core_btc = 0.5
trading_btc = 0.1
cash = 20000

INITIAL_CAPITAL = None   # auto set ครั้งแรก
peak_equity = None


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


def run_cycle():
    global peak_equity, INITIAL_CAPITAL

    init_crypto_db()

    btc_price = get_latest_price()

    if btc_price is None:
        print("No BTC price data yet")
        return

    # ===== REGIME =====
    regime = get_regime()
    trading_weight = trading_btc_weight_of_portfolio(regime)

    # ===== PORTFOLIO VALUE =====
    total_equity = calculate_portfolio_value(
        btc_price,
        core_btc,
        trading_btc,
        cash
    )

    # ===== SET INITIAL CAPITAL FIRST TIME =====
    if INITIAL_CAPITAL is None:
        INITIAL_CAPITAL = total_equity

    pnl = total_equity - INITIAL_CAPITAL
    pnl_pct = (pnl / INITIAL_CAPITAL) * 100

    # ===== PEAK TRACK =====
    if peak_equity is None:
        peak_equity = total_equity

    if total_equity > peak_equity:
        peak_equity = total_equity

    # ===== RISK =====
    risk_trigger, dd = check_drawdown(total_equity, peak_equity)

    # ===== CORE DECISION =====
    core_value = core_btc * btc_price

    core_decision = core_action(
        regime,
        core_value,
        total_equity,
        cash
    )

    # ===== MOMENTUM =====
    current_weight = get_btc_weight(
        btc_price,
        core_btc,
        trading_btc,
        cash
    )

    target_weight = calc_target_weight(current_weight)

    # ===== HOLDING DETAIL =====
    btc_amount = core_btc + trading_btc
    btc_value = btc_amount * btc_price

    btc_weight_pct = (btc_value / total_equity) * 100
    cash_weight_pct = (cash / total_equity) * 100

    target_pct = target_weight * 100
    diff_pct = target_pct - btc_weight_pct

    # ===== OUTPUT =====
    print("\n====== STATUS ======")
    print("BTC price:", round(btc_price, 2))
    print("Regime:", regime)
    print("Trading BTC Weight:", trading_weight)

    print("\n------ PORTFOLIO ------")
    print("Initial Capital :", round(INITIAL_CAPITAL, 2))
    print("Current Equity  :", round(total_equity, 2))
    print("PnL             :", round(pnl, 2), f"({round(pnl_pct,2)}%)")

    print("\n------ HOLDINGS ------")
    print("BTC amount      :", round(btc_amount, 4))
    print("BTC value       :", round(btc_value, 2))
    print("Cash            :", round(cash, 2))

    print("\n------ ALLOCATION ------")
    print("BTC weight      :", round(btc_weight_pct, 2), "%")
    print("Cash weight     :", round(cash_weight_pct, 2), "%")
    print("Target BTC      :", round(target_pct, 2), "%")
    print("Rebalance diff  :", round(diff_pct, 2), "%")

    print("\n------ RISK ------")
    print("Drawdown        :", round(dd, 4))
    print("Risk Trigger    :", risk_trigger)


if __name__ == "__main__":
    run_cycle()