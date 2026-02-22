import schedule
import time

from portfolios.trend_port.engine import run_bot
from portfolios.trend_port.risk_automation import intraday_risk_check


def start_scheduler():

    schedule.every().day.at("21:15").do(run_bot)
    schedule.every(5).minutes.do(intraday_risk_check)

    print("🚀 Athena Automation Started")

    while True:
        schedule.run_pending()
        time.sleep(20)