from portfolios.crypto_port.config import CORE_TARGET

def core_action(regime, current_core_value, total_portfolio_value, cash):

    if total_portfolio_value == 0:
        return {"action": "HOLD"}

    core_weight = current_core_value / total_portfolio_value

    if regime != "BEAR":
        return {"action": "HOLD"}

    if core_weight >= CORE_TARGET:
        return {"action": "HOLD"}

    if cash <= total_portfolio_value * 0.05:
        return {"action": "HOLD"}

    target_core_value = total_portfolio_value * CORE_TARGET
    value_gap = target_core_value - current_core_value

    max_step = total_portfolio_value * 0.02

    buy_value = min(value_gap, max_step)

    return {
        "action": "BUY",
        "btc_value": buy_value
    }
