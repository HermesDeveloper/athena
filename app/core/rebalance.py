import yfinance as yf
from datetime import datetime
import sqlite3

from alpaca.data.historical import StockHistoricalDataClient
from alpaca.data.requests import StockLatestQuoteRequest

from portfolios.trend_port.strategy.trend import (
    trend_allowed,
    exit_signal,
    breakout_boost
)

from config.settings import (
    ALPACA_KEY,
    ALPACA_SECRET,
    ASSETS,
    ALLOCATION_RATIO,
    REBALANCE_THRESHOLD,
    PARTIAL_RATIO,
    SAFETY_BUYING_POWER_CAP,
    TREND_DB_PATH
)

from portfolios.trend_port.execution.alpaca_client import (
    get_account,
    get_positions,
    submit_market
)

# =========================================
# PRICE CLIENT
# =========================================

data_client = StockHistoricalDataClient(ALPACA_KEY, ALPACA_SECRET)


def get_latest_price(symbol: str):
    try:
        request = StockLatestQuoteRequest(symbol_or_symbols=symbol)
        quote = data_client.get_stock_latest_quote(request)
        return float(quote[symbol].ask_price)
    except Exception:
        return 0


# =========================================
# FLATTEN ALLOCATION
# =========================================

def flatten_assets():
    flat = {}
    for group, symbols in ASSETS.items():
        group_ratio = ALLOCATION_RATIO.get(group, 0)
        for sym, weight in symbols.items():
            flat[sym] = flat.get(sym, 0) + group_ratio * weight
    return flat


# =========================================
# LOG ORDER
# =========================================

def log_order(symbol, side, qty, price):
    conn = sqlite3.connect(TREND_DB_PATH)
    c = conn.cursor()

    c.execute("""
        INSERT INTO order_log VALUES (?, ?, ?, ?, ?)
    """, (
        datetime.now().isoformat(),
        symbol,
        side,
        qty,
        price
    ))

    conn.commit()
    conn.close()


# =========================================
# AGGRESSIVE TACTICAL REBALANCE
# =========================================

def rebalance(target_exposure: float, dry_run=False):

    account = get_account()
    equity = float(account.equity)
    buying_power = float(account.buying_power)

    max_allowed_bp = buying_power * SAFETY_BUYING_POWER_CAP
    target_invest_value = equity * target_exposure

    flat = flatten_assets()
    positions = get_positions()

    current_map = {}
    for p in positions:
        current_map[p.symbol] = int(float(p.qty))

    print("\n===== AGGRESSIVE TACTICAL REBALANCE =====")
    print(f"Equity: {equity:,.2f}")
    print(f"Target Exposure: {target_exposure:.2f}")
    print(f"Buying Power Cap: {max_allowed_bp:,.2f}")
    print("==========================================\n")

    for sym, weight in flat.items():

        # -------------------------------
        # LOAD TREND DATA (once per symbol)
        # -------------------------------
        df = yf.download(sym, period="6mo", progress=False)

        if df.empty:
            print(f"{sym}: No data → Skip")
            continue

        current_qty = current_map.get(sym, 0)

        # -------------------------------
        # EXIT / REDUCE FIRST
        # -------------------------------
        signal = exit_signal(df)

        if signal == "EXIT" and current_qty > 0:
            print(f"{sym}: EXIT signal → Sell ALL ({current_qty})")
            if not dry_run:
                submit_market(sym, current_qty, "SELL")
                log_order(sym, "SELL", current_qty, df["Close"].iloc[-1])
            continue

        if signal == "REDUCE" and current_qty > 0:
            reduce_qty = int(current_qty * 0.5)
            if reduce_qty > 0:
                print(f"{sym}: REDUCE signal → Sell {reduce_qty}")
                if not dry_run:
                    submit_market(sym, reduce_qty, "SELL")
                    log_order(sym, "SELL", reduce_qty, df["Close"].iloc[-1])
            continue

        # -------------------------------
        # TREND FILTER
        # -------------------------------
        if not trend_allowed(df):
            print(f"{sym}: Trend not allowed → Skip")
            continue

        # -------------------------------
        # PRICE & TARGET CALC
        # -------------------------------
        price = get_latest_price(sym)
        if price <= 0:
            print(f"{sym}: No live price → Skip")
            continue

        target_value = target_invest_value * weight
        target_qty = int(target_value / price)

        # Breakout Boost
        boost = breakout_boost(df)
        target_qty = int(target_qty * boost)

        diff_qty = target_qty - current_qty

        if current_qty > 0:
            deviation = abs(diff_qty) / max(current_qty, 1)
        else:
            deviation = 1

        # -------------------------------
        # THRESHOLD FILTER
        # -------------------------------
        if deviation < REBALANCE_THRESHOLD:
            continue

        # -------------------------------
        # PARTIAL EXECUTION
        # -------------------------------
        diff_qty = int(diff_qty * PARTIAL_RATIO)

        if diff_qty == 0:
            continue

        side = "BUY" if diff_qty > 0 else "SELL"

        # -------------------------------
        # SAFETY BUYING POWER
        # -------------------------------
        if side == "BUY":
            order_value = abs(diff_qty) * price
            if order_value > max_allowed_bp:
                print(f"{sym}: Skipped (Buying Power Limit)")
                continue

        print(
            f"{sym} | Price={price:.2f} | "
            f"Target={target_qty} | "
            f"Current={current_qty} | "
            f"{side} {abs(diff_qty)}"
        )

        if not dry_run:
            submit_market(sym, abs(diff_qty), side)
            log_order(sym, side, abs(diff_qty), price)

    print("\n===== REBALANCE COMPLETE =====\n")
