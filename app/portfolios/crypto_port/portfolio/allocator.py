# portfolio/allocator.py

from portfolios.crypto_port.config import CORE_TARGET, TRADING_TARGET, CASH_TARGET


# =========================
# TARGET ALLOCATION
# =========================
def get_target_allocation():
    total = CORE_TARGET + TRADING_TARGET + CASH_TARGET

    if abs(total - 1.0) > 0.0001:
        raise ValueError("Target allocation must sum to 1")

    return {
        "core": CORE_TARGET,
        "trading": TRADING_TARGET,
        "cash": CASH_TARGET
    }


# =========================
# TOTAL PORTFOLIO VALUE
# =========================
def calculate_portfolio_value(btc_price, core_btc, trading_btc, cash):
    return (core_btc + trading_btc) * btc_price + cash


# =========================
# 🔹 1) FULL PORTFOLIO WEIGHTS (DICT)
# =========================
def get_portfolio_weights(btc_price, core_btc, trading_btc, cash):
    """
    คืน dict สัดส่วนทั้งพอร์ต
    {
        core: float,
        trading: float,
        cash: float
    }
    """

    total = calculate_portfolio_value(
        btc_price, core_btc, trading_btc, cash
    )

    if total == 0:
        return {
            "core": 0.0,
            "trading": 0.0,
            "cash": 0.0
        }

    return {
        "core": (core_btc * btc_price) / total,
        "trading": (trading_btc * btc_price) / total,
        "cash": cash / total
    }


# =========================
# 🔹 2) BTC TOTAL WEIGHT (FLOAT)
# =========================
def get_btc_weight(btc_price, core_btc, trading_btc, cash):
    """
    คืน BTC weight รวมทั้ง core + trading
    ใช้กับ momentum engine
    """

    btc_value = (core_btc + trading_btc) * btc_price
    total_value = btc_value + cash

    if total_value == 0:
        return 0.0

    return btc_value / total_value