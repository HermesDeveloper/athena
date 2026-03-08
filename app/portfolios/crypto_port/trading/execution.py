from portfolios.crypto_port.binance_client import get_client

client = get_client()

BTC_PRECISION = 5
USDT_PRECISION = 2

MIN_BUY_USDT = 10
MIN_SELL_BTC = 0.00001


def format_btc(qty):
    return float(f"{qty:.{BTC_PRECISION}f}")


def format_usdt(value):
    return float(f"{value:.{USDT_PRECISION}f}")


# =============================
# GET BALANCE
# =============================

def get_balance():

    try:

        account = client.get_account()

        btc = 0
        usdt = 0

        for asset in account["balances"]:

            if asset["asset"] == "BTC":
                btc = float(asset["free"])

            if asset["asset"] == "USDT":
                usdt = float(asset["free"])

        return btc, usdt

    except Exception as e:

        print("BALANCE ERROR:", e)

        return 0, 0


# =============================
# BUY BTC
# =============================

def buy_btc(usdt_value):

    usdt_value = format_usdt(usdt_value)

    if usdt_value < MIN_BUY_USDT:
        print("Buy amount too small")
        return None

    try:

        order = client.order_market_buy(
            symbol="BTCUSDT",
            quoteOrderQty=usdt_value
        )

        print("\nBUY ORDER EXECUTED")
        print("USDT used:", usdt_value)

        return order

    except Exception as e:

        print("\nBUY ERROR:", e)

        return None


# =============================
# SELL BTC
# =============================

def sell_btc(quantity):

    quantity = format_btc(quantity)

    if quantity < MIN_SELL_BTC:
        print("Sell amount too small")
        return None

    try:

        order = client.order_market_sell(
            symbol="BTCUSDT",
            quantity=quantity
        )

        print("\nSELL ORDER EXECUTED")
        print("BTC sold:", quantity)

        return order

    except Exception as e:

        print("\nSELL ERROR:", e)

        return None