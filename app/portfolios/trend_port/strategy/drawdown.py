def drawdown_trigger(
    peak_value: float,
    current_value: float,
    max_dd: float = -0.15
) -> bool:
    dd = (current_value - peak_value) / peak_value
    return dd <= max_dd
