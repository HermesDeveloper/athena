import time
import os
import platform
from datetime import datetime

from portfolios.crypto_port.data.fetch_binance import fetch_and_store
from portfolios.crypto_port.main import run_cycle


def clear_screen():
    if platform.system() == "Windows":
        os.system("cls")
    else:
        os.system("clear")


def run():
    print("=== Athena Crypto Engine Started ===")

    while True:
        try:
            clear_screen()

            print("===================================")
            print("Time:", datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
            print("===================================")

            # ดึงราคาใหม่
            fetch_and_store()

            # รัน logic พอร์ต
            run_cycle()

        except Exception as e:
            print("ERROR:", e)

        print("\nNext update in 5 minutes...")
        time.sleep(300)


if __name__ == "__main__":
    run()