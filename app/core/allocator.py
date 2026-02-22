from config.settings import (
    TARGET_EXPOSURE,
    ALLOCATION_RATIO,
    ASSETS,
    CRYPTO_CAP
)

def get_target_exposure(market_state):
    return TARGET_EXPOSURE.get(market_state, 0.40)


def build_target_portfolio(market_state):
    """
    return:
    {
        "NVDA": 0.126,
        "MSFT": 0.105,
        ...
        "GLD": 0.14,
        "BTC": 0.07,
        "CASH": 0.30
    }
    """

    exposure = get_target_exposure(market_state)
    portfolio = {}

    # ===== US EQUITY =====
    us_equity_budget = exposure * ALLOCATION_RATIO["US_EQUITY"]

    for symbol, weight in ASSETS["US_EQUITY"].items():
        portfolio[symbol] = us_equity_budget * weight

    # ===== METAL =====
    metal_budget = exposure * ALLOCATION_RATIO["METAL"]
    for symbol in ASSETS["METAL"]:
        portfolio[symbol] = metal_budget

    # ===== CRYPTO (DYNAMIC CAP) =====
    crypto_budget = min(
        exposure * ALLOCATION_RATIO["CRYPTO"],
        CRYPTO_CAP[market_state]
    )

    for symbol in ASSETS["CRYPTO"]:
        portfolio[symbol] = crypto_budget

    # ===== CASH =====
    invested = sum(portfolio.values())
    portfolio["CASH"] = round(1 - invested, 4)

    return portfolio
