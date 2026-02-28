import schedule
import time
import traceback

from portfolios.trend_port.engine import run_bot
from portfolios.trend_port.risk_automation import intraday_risk_check


def safe_run(job_func, name):
    try:
        job_func()
    except Exception as e:
        print(f"[SCHEDULER ERROR] {name} → {e}")
        traceback.print_exc()


def start_scheduler():

    schedule.every().day.at("21:15").do(lambda: safe_run(run_bot, "run_bot"))
    schedule.every(5).minutes.do(lambda: safe_run(intraday_risk_check, "risk_check"))

    print("🚀 Athena Automation Started")

    while True:
        try:
            schedule.run_pending()
        except Exception as loop_error:
            print(f"[LOOP ERROR] {loop_error}")
            traceback.print_exc()

        time.sleep(20)