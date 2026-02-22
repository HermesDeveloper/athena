import sqlite3
import os

from config.settings import QUANT_DB_PATH


def init_db():
    os.makedirs("data", exist_ok=True)

    conn = sqlite3.connect(QUANT_DB_PATH)
    c = conn.cursor()

    c.execute("""
        CREATE TABLE IF NOT EXISTS stocks (
            ticker TEXT PRIMARY KEY,
            source TEXT,
            market_cap REAL,
            revenue_cagr REAL,
            net_margin REAL,
            pe REAL,
            pb REAL,
            debt_equity REAL,
            roe REAL,
            roa REAL,
            fcf_positive INTEGER,
            fcf_growth INTEGER,
            ocf_vs_income INTEGER,
            cf_to_debt REAL,
            peg_ratio REAL,
            fcf_yield REAL,
            undervalued_score REAL,
            score INTEGER
        )
    """)

    conn.commit()
    conn.close()


def upsert_stock(data):
    conn = sqlite3.connect(QUANT_DB_PATH)
    c = conn.cursor()

    c.execute("""
        INSERT INTO stocks VALUES (
            :ticker, :source, :market_cap, :revenue_cagr, :net_margin,
            :pe, :pb, :debt_equity, :roe, :roa,
            :fcf_positive, :fcf_growth,
            :ocf_vs_income, :cf_to_debt,
            :peg_ratio, :fcf_yield, :undervalued_score,
            :score
        )
        ON CONFLICT(ticker) DO UPDATE SET
            source=excluded.source,
            market_cap=excluded.market_cap,
            revenue_cagr=excluded.revenue_cagr,
            net_margin=excluded.net_margin,
            pe=excluded.pe,
            pb=excluded.pb,
            debt_equity=excluded.debt_equity,
            roe=excluded.roe,
            roa=excluded.roa,
            fcf_positive=excluded.fcf_positive,
            fcf_growth=excluded.fcf_growth,
            ocf_vs_income=excluded.ocf_vs_income,
            cf_to_debt=excluded.cf_to_debt,
            peg_ratio=excluded.peg_ratio,
            fcf_yield=excluded.fcf_yield,
            undervalued_score=excluded.undervalued_score,
            score=excluded.score
    """, data)

    conn.commit()
    conn.close()
