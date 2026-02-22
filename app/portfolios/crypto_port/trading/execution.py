# trading/execution.py

import ccxt
import os


def get_exchange():
    exchange = ccxt.binance({
        "apiKey": os.getenv("BINANCE_API_KEY"),
        "secret": os.getenv("BINANCE_SECRET"),
        "enableRateLimit": True,
        "options": {
            "defaultType": "future"
        }
    })

    # 🔐 ใช้ testnet
    exchange.set_sandbox_mode(True)

    return exchange



def market_buy(symbol, amount):
    exchange = get_exchange()
    order = exchange.create_market_buy_order(symbol, amount)
    return order


def market_sell(symbol, amount):
    exchange = get_exchange()
    order = exchange.create_market_sell_order(symbol, amount)
    return order


def paper_buy(symbol, amount, price):
    return {
        "symbol": symbol,
        "amount": amount,
        "price": price,
        "status": "FILLED",
        "mode": "PAPER"
    }
