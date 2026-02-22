from portfolios.crypto_port.config import MAX_DRAWDOWN


def check_drawdown(current_equity, peak_equity):

    # 🔐 ป้องกันหารศูนย์
    if peak_equity <= 0:
        return False, 0.0

    dd = (peak_equity - current_equity) / peak_equity

    if dd > MAX_DRAWDOWN:
        return True, dd

    return False, dd

def risk_multiplier(dd):

    if dd < 0.10:
        return 1.0
    elif dd < 0.20:
        return 0.7
    elif dd < 0.30:
        return 0.4
    else:
        return 0.0
