from core.rebalance import rebalance
from portfolios.trend_port.execution.alpaca_client import get_account
from core.database_logger import log_market_snapshot
from core.risk import detect_crash, calculate_target_exposure


def run_bot():

    market_state = detect_crash()
    exposure = calculate_target_exposure(market_state)

    account = get_account()
    equity = float(account.equity)
    buying_power = float(account.buying_power)

    print("Crash:", market_state)
    print("Target exposure:", exposure)
    print("Equity:", equity)
    print("Buying Power:", buying_power)

    log_market_snapshot(market_state, exposure, equity)

    rebalance(exposure, dry_run=False)
