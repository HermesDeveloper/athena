import yfinance as yf

def vix_high(threshold=25) -> bool:
    vix = yf.download("^VIX", period="5d", interval="1d")
    if vix.empty:
        return False

    return vix["Close"].iloc[-1] > threshold
