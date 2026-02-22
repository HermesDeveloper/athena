from core.database import init_db
from portfolios.trend_port.engine import run_bot
from portfolios.trend_port.scheduler import start_scheduler


if __name__ == "__main__":

    init_db()

    MODE = "scheduler"  # "run_once" หรือ "scheduler"

    if MODE == "run_once":
        run_bot()

    elif MODE == "scheduler":
        start_scheduler()
