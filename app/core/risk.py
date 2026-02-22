import yfinance as yf
from config.settings import TARGET_EXPOSURE

# ========= MARKET CRASH =========
def detect_crash():
    spy = yf.download("SPY", period="1d", interval="5m", progress=False)

    if spy.empty or len(spy) < 2:
        return "NORMAL"

    # ดึง close แบบปลอดภัย
    close = spy["Close"]

    # ถ้าเป็น DataFrame (multi column) ให้เลือกคอลัมน์แรก
    if hasattr(close, "columns"):
        close = close.iloc[:, 0]

    first_price = close.iloc[0].item()
    last_price = close.iloc[-1].item()

    change = (last_price - first_price) / first_price

    if change < -0.035:
        return "SEVERE"
    elif change < -0.02:
        return "CRASH"

    return "NORMAL"



# ========= EXPOSURE DECISION =========
def calculate_target_exposure(
    market_state: str,
    vix_high: bool = False,
    drawdown_triggered: bool = False
) -> float:
    exposure = TARGET_EXPOSURE.get(market_state, 0.40)

    if vix_high:
        exposure *= 0.8  # ลด 20%

    if drawdown_triggered:
        exposure = min(exposure, 0.40)

    return round(exposure, 2)
