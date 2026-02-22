import sqlite3
import pandas as pd
import yfinance as yf
import time

from research.quant_score.universe_loader import load_symbols_from_txt
from research.quant_score.metrics import calculate_cagr
from research.quant_score.scoring_engine import calculate_score
from research.quant_score.database import init_db, upsert_stock
from research.quant_score.config import SP600_FILE, NASDAQ_FILE
from config.settings import QUANT_DB_PATH


def process_all_stocks():

    symbols_sp600 = load_symbols_from_txt(SP600_FILE)
    symbols_nasdaq = load_symbols_from_txt(NASDAQ_FILE)

    # รวม + ระบุ source
    symbols = {}

    for s in symbols_sp600:
        symbols[s] = "SP600"

    for s in symbols_nasdaq:
        symbols[s] = "NASDAQ"

    symbols_list = list(symbols.items())
    total = len(symbols_list)

    print(f"\nTotal Stocks: {total}")
    print("-" * 70)

    for i, (ticker, source) in enumerate(symbols_list, start=1):

        percent = (i / total) * 100
        print(f"[{i}/{total}] ({percent:.1f}%) Reading {ticker} ({source})")

        try:
            stock = yf.Ticker(ticker)
            info = stock.info
            financials = stock.financials
            cashflow = stock.cashflow

            # ---------------- Defaults ----------------
            data = {
                "ticker": ticker,
                "source": source,
                "market_cap": info.get("marketCap", 0),
                "revenue_cagr": 0,
                "net_margin": info.get("profitMargins", 0),
                "pe": info.get("trailingPE", 0),
                "pb": info.get("priceToBook", 0),
                "debt_equity": info.get("debtToEquity", 0),
                "roe": info.get("returnOnEquity", 0),
                "roa": info.get("returnOnAssets", 0),
                "fcf_positive": 0,
                "fcf_growth": 0,
                "ocf_vs_income": 0,
                "cf_to_debt": 0,
                "peg_ratio": 0,
                "fcf_yield": 0,
                "undervalued_score": 0,
                "score": 0
            }

            # ---------------- Revenue CAGR (5Y) ----------------
            if not financials.empty and "Total Revenue" in financials.index:

                rev_series = financials.loc["Total Revenue"].sort_index()
                rev_series = rev_series.tail(5)

                if len(rev_series) == 5:
                    cagr = calculate_cagr(rev_series)
                    data["revenue_cagr"] = cagr if cagr else 0

     


            # ---------------- PEG (Guard: growth > 5%) ----------------
            if data["revenue_cagr"] > 0.05 and data["pe"] > 0:
                growth_percent = data["revenue_cagr"] * 100
                data["peg_ratio"] = data["pe"] / growth_percent


            # ---------------- Cash Flow ----------------
            if not cashflow.empty:

                # FCF 5 ปี
                if "Free Cash Flow" in cashflow.index:

                    fcf = cashflow.loc["Free Cash Flow"].sort_index().tail(5)
                    fcf = fcf.dropna()

                    if len(fcf) == 5 and (fcf > 0).all():
                        data["fcf_positive"] = 1

                    if len(fcf) >= 2 and fcf.iloc[-1] > fcf.iloc[0]:
                        data["fcf_growth"] = 1

                    # FCF Yield
                    if data["market_cap"] > 0:
                        latest_fcf = fcf.iloc[-1]
                        data["fcf_yield"] = latest_fcf / data["market_cap"]

                # OCF vs Net Income
                if "Operating Cash Flow" in cashflow.index and "Net Income" in financials.index:

                    ocf = cashflow.loc["Operating Cash Flow"].iloc[0]
                    net_income = financials.loc["Net Income"].iloc[0]

                    if ocf > net_income:
                        data["ocf_vs_income"] = 1

                # ---------------- Undervalued Score (Guard) ----------------
                if data["peg_ratio"] > 0 and data["fcf_yield"] > 0:
                        data["undervalued_score"] = (
                        data["fcf_yield"] / (data["peg_ratio"] + 0.1)
                        )



            # ---------------- Final Score ----------------
            data["score"] = calculate_score(data)

            upsert_stock(data)

        except Exception as e:
            print(f"Error {ticker}: {e}")


def show_top():

    conn = sqlite3.connect(QUANT_DB_PATH)
    df = pd.read_sql("SELECT * FROM stocks ORDER BY score DESC", conn)
    conn.close()

    if df.empty:
        print("No data in DB")
        return

    # แปลงเป็น %
    df["net_margin_%"] = (df["net_margin"] * 100).round(2)
    df["revenue_cagr_%"] = (df["revenue_cagr"] * 100).round(2)
    df["fcf_yield_%"] = (df["fcf_yield"] * 100).round(2)
    df["peg"] = df["peg_ratio"].round(2)
    df["undervalued"] = df["undervalued_score"].round(4)

    pd.set_option('display.max_rows', 200)
    pd.set_option('display.max_columns', None)
    pd.set_option('display.width', None)

    print("\n===== TOP 100 STOCKS =====")
    print(
        df.head(100)[
            [
                "ticker",
                "source",
                "score",
                "revenue_cagr_%",
                "net_margin_%",
                "peg",
                "fcf_yield_%",
                "undervalued"
            ]
        ].to_string(index=False)
    )


if __name__ == "__main__":
    init_db()
    process_all_stocks()
    show_top()
