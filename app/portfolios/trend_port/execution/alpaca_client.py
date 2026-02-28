import time
from alpaca.trading.client import TradingClient
from alpaca.trading.requests import MarketOrderRequest
from alpaca.trading.enums import OrderSide, TimeInForce
from config.settings import ALPACA_KEY, ALPACA_SECRET, BASE_URL


# ===============================
# CLIENT (singleton)
# ===============================

_client = None

def get_client():
    global _client
    if _client is None:
        _client = TradingClient(
            api_key=ALPACA_KEY,
            secret_key=ALPACA_SECRET,
            paper="paper" in BASE_URL
        )
    return _client


# ===============================
# SAFE WRAPPER
# ===============================

def _retry(func, retries=3, delay=2):
    for i in range(retries):
        try:
            return func()
        except Exception as e:
            print(f"[ALPACA RETRY {i+1}/{retries}] {e}")
            time.sleep(delay)
    return None


# ===============================
# ACCOUNT
# ===============================

def get_account():
    return _retry(lambda: get_client().get_account())


def get_positions():
    return _retry(lambda: get_client().get_all_positions())


# ===============================
# ORDER
# ===============================

def submit_market(symbol: str, qty: float, side: str):
    if qty <= 0:
        return None

    def _submit():
        order = MarketOrderRequest(
            symbol=symbol,
            qty=abs(qty),
            side=OrderSide.BUY if side == "BUY" else OrderSide.SELL,
            time_in_force=TimeInForce.DAY
        )
        return get_client().submit_order(order)

    return _retry(_submit)


def buy(symbol, qty):
    return submit_market(symbol, qty, "BUY")


def sell(symbol, qty):
    return submit_market(symbol, qty, "SELL")