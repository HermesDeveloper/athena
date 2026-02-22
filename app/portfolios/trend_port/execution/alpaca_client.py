from alpaca.trading.client import TradingClient
from alpaca.trading.requests import MarketOrderRequest
from alpaca.trading.enums import OrderSide, TimeInForce
from config.settings import ALPACA_KEY, ALPACA_SECRET, BASE_URL


# ===============================
# CLIENT
# ===============================

def get_client():
    return TradingClient(
        api_key=ALPACA_KEY,
        secret_key=ALPACA_SECRET,
        paper="paper" in BASE_URL
    )


# ===============================
# ACCOUNT
# ===============================

def get_account():
    return get_client().get_account()


def get_positions():
    return get_client().get_all_positions()


# ===============================
# ORDER
# ===============================

def submit_market(symbol: str, qty: float, side: str):
    if qty <= 0:
        return None

    client = get_client()

    order = MarketOrderRequest(
        symbol=symbol,
        qty=abs(qty),
        side=OrderSide.BUY if side == "BUY" else OrderSide.SELL,
        time_in_force=TimeInForce.DAY
    )

    return client.submit_order(order)


def buy(symbol, qty):
    return submit_market(symbol, qty, "BUY")


def sell(symbol, qty):
    return submit_market(symbol, qty, "SELL")
