from binance.client import Client
import time

from config.binance_config import (
    BINANCE_API_KEY,
    BINANCE_SECRET_KEY,
    BINANCE_BASE_URL
)


def get_client():

    client = Client(
        BINANCE_API_KEY,
        BINANCE_SECRET_KEY
    )

    # ใช้ Binance Testnet
    client.API_URL = BINANCE_BASE_URL

    # 🔹 sync เวลาเครื่องกับ server Binance
    server_time = client.get_server_time()["serverTime"]
    local_time = int(time.time() * 1000)

    client.timestamp_offset = server_time - local_time

    return client