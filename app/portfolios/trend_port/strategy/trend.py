import pandas as pd


def _clean_close(df: pd.DataFrame) -> pd.Series:
    close = df["Close"]

    # ถ้าเป็น DataFrame (multi-column) ให้เลือก column แรก
    if isinstance(close, pd.DataFrame):
        close = close.iloc[:, 0]

    return close


# ========= TREND FILTER =========
def trend_allowed(df: pd.DataFrame) -> bool:

    close = _clean_close(df)

    ma20 = close.rolling(20).mean()
    ma50 = close.rolling(50).mean()
    ma200 = close.rolling(200).mean()

    if pd.isna(ma50.iloc[-1]) or pd.isna(ma200.iloc[-1]):
        return False

    return (
        ma50.iloc[-1] > ma200.iloc[-1]
        and close.iloc[-1] > ma20.iloc[-1]
    )


# ========= EXIT / DE-RISK =========
def exit_signal(df: pd.DataFrame) -> str:

    close = _clean_close(df)

    ma50 = close.rolling(50).mean()
    ma200 = close.rolling(200).mean()

    last_close = close.iloc[-1]
    ma50_last = ma50.iloc[-1]
    ma200_last = ma200.iloc[-1]

    if pd.isna(ma50_last) or pd.isna(ma200_last):
        return "HOLD"

    if last_close < ma200_last:
        return "EXIT"

    if last_close < ma50_last:
        return "REDUCE"

    return "HOLD"


# ========= BREAKOUT BOOST =========
def breakout_boost(df: pd.DataFrame) -> float:

    high = df["High"]

    if isinstance(high, pd.DataFrame):
        high = high.iloc[:, 0]

    close = _clean_close(df)

    high_3m = high.rolling(63).max()

    if close.iloc[-1] > high_3m.iloc[-2]:
        return 1.15

    return 1.0
