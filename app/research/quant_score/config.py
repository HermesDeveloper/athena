import os

BASE_DIR = os.path.dirname(__file__)

SP600_FILE = os.path.join(BASE_DIR, "data", "S&P_600_stock.txt")
NASDAQ_FILE = os.path.join(BASE_DIR, "data", "NASDAQ_List.txt")




MIN_MARKET_CAP = 300_000_000
MAX_MARKET_CAP = 5_000_000_000

YEARS_LOOKBACK = 5



