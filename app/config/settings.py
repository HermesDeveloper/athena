import os


# ===== DATABASE =====
BASE_DIR = os.path.dirname(os.path.dirname(__file__))

TREND_DB_PATH = os.path.join(BASE_DIR, "data", "trend.db")

QUANT_DB_PATH = os.path.join(
    BASE_DIR,
    "research",
    "quant_score",
    "data",
    "quant_score.db"
)


CRYPTO_DB_PATH = os.path.join(
    BASE_DIR,
    "portfolios",
    "crypto_port",
    "data",
    "crypto.db"
)


# ===== BROKER =====
ALPACA_KEY = "PKEXXX5JQR4XNKWGPSZNVQXFY4"
ALPACA_SECRET = "GsbwmXKVAcJu9sSbkPK1Q6QYaeRJ68fJDVqHR51jm2n3"

ENV = "PAPER"  # PAPER / LIVE

BASE_URLS = {
    "PAPER": "https://paper-api.alpaca.markets",
    "LIVE": "https://api.alpaca.markets"
}

BASE_URL = BASE_URLS[ENV]


# ===== TACTICAL SETTINGS =====

REBALANCE_THRESHOLD = 0.05      # 5% deviation
PARTIAL_RATIO = 0.5             # ยิงครึ่งเดียวของ diff
SAFETY_BUYING_POWER_CAP = 0.85  # ใช้ buying power ไม่เกิน 85%




# ===== MARKET RISK STATES =====
MARKET_STATE = {
    "NORMAL": "NORMAL",
    "CRASH": "CRASH",
    "SEVERE": "SEVERE"
}

# ===== TARGET EXPOSURE BY MARKET STATE =====
TARGET_EXPOSURE = {
    "NORMAL": 0.70,
    "CRASH": 0.50,
    "SEVERE": 0.40
}

# ===== ASSET GROUPS =====
ASSETS = {
    "US_EQUITY": {
        "NVDA": 0.18,
        "MSFT": 0.15,
        "QQQ":  0.15,
        "AVGO": 0.10,
        "AMD":  0.05,
        "LMT":  0.07
    },
    "METAL": {
        "GLD": 1.00   # internal weight
    },
"CRYPTO": {
    "IBIT": 1.00
}
}

# ===== ALLOCATION INSIDE EXPOSURE =====
ALLOCATION_RATIO = {
    "US_EQUITY": 0.70,
    "METAL": 0.20,
    "CRYPTO": 0.10
}

# ===== CRYPTO DYNAMIC CAP =====
CRYPTO_CAP = {
    "NORMAL": 0.10,
    "CRASH": 0.05,
    "SEVERE": 0.02
}


# ===== RISK AUTOMATION =====

DD_LEVEL_1 = 0.04   # 4% drawdown
DD_LEVEL_2 = 0.06   # 6%
DD_LEVEL_3 = 0.08   # 8%
DD_LEVEL_4 = 0.10   # 10%

REDUCE_L1 = 0.30
REDUCE_L2 = 0.50
REDUCE_L3 = 0.80
REDUCE_L4 = 0.95
