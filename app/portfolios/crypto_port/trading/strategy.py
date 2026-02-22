from portfolios.crypto_port.config import (
    TRADING_TARGET,
    BULL_INTERNAL_WEIGHT,
    BEAR_INTERNAL_WEIGHT
)

def trading_btc_weight_within_trading(regime):
    """
    ภายใน Trading bucket ควรถือ BTC กี่ %
    """
    if regime == "BULL":
        return BULL_INTERNAL_WEIGHT
    return BEAR_INTERNAL_WEIGHT


def trading_btc_weight_of_portfolio(regime):
    """
    BTC จาก Trading คิดเป็นกี่ % ของพอร์ตทั้งหมด
    """
    internal_weight = trading_btc_weight_within_trading(regime)
    return TRADING_TARGET * internal_weight
