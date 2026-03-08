from portfolio.allocator import get_target_allocation


REBALANCE_TOLERANCE = 0.02  # 2% deviation


def rebalance_portfolio(btc_price, core_btc, trading_btc, cash):

    if btc_price <= 0:
        return {"action": "HOLD"}

    targets = get_target_allocation()

    total_value = (core_btc + trading_btc) * btc_price + cash

    if total_value == 0:
        return {"action": "HOLD"}

    target_core_value = total_value * targets["core"]
    target_trading_value = total_value * targets["trading"]

    current_core_value = core_btc * btc_price
    current_trading_value = trading_btc * btc_price

    core_diff = target_core_value - current_core_value
    trading_diff = target_trading_value - current_trading_value

    # 🔹 tolerance guard
    if abs(core_diff) / total_value < REBALANCE_TOLERANCE and \
       abs(trading_diff) / total_value < REBALANCE_TOLERANCE:
        return {"action": "HOLD"}

    # 🔹 prevent over-buy beyond cash
    total_buy_needed = max(0, core_diff) + max(0, trading_diff)

    if total_buy_needed > cash:
        scale = cash / total_buy_needed
        core_diff *= scale
        trading_diff *= scale

    return {
        "action": "REBALANCE",
        "core_btc_diff": core_diff / btc_price,
        "trading_btc_diff": trading_diff / btc_price
    }

    