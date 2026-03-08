import time
import os
import platform
import traceback

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
            print("Time:", datetime.now())
            print("===================================")

            fetch_and_store()

            run_cycle()

        except Exception as e:

                print("\n ERROR OCCURRED")
                traceback.print_exc()

        print("Next update in 30 minutes...")

        time.sleep(1800)


if __name__ == "__main__":
    run()