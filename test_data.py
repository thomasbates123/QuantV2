import yfinance as yf
import pandas as pd
import sqlite3
from datetime import date

# Connect (creates db if it doesn’t exist)
conn = sqlite3.connect("options_data.db")

def collect_options(ticker_symbol):
    ticker = yf.Ticker(ticker_symbol)
    all_data = []

    for expiry in ticker.options:
        chain = ticker.option_chain(expiry)
        for option_type, df in [("call", chain.calls), ("put", chain.puts)]:
            df = df.copy()
            df["ticker"] = ticker_symbol
            df["expiry"] = expiry
            df["type"] = option_type
            df["snapshot_date"] = date.today().isoformat()
            all_data.append(df)

    return pd.concat(all_data, ignore_index=True)

# Example: collect AAPL
df = collect_options("AAPL")

# Save to SQL
df.to_sql("options_data", conn, if_exists="append", index=False)

print("Saved", len(df), "rows")
print(df.head())