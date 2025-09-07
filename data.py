import yfinance as yf
import pandas as pd
import sqlite3
from datetime import date

# Connect (creates db if it doesn’t exist)
conn = sqlite3.connect("options_data.db")


# load data
df = pd.read_sql("SELECT * FROM options_data", conn)

print(df.head())


# Convert 'snapshot' column to datetime if it's not already
df['snapshot'] = pd.to_datetime(df['snapshot'])

# Get the most recent date
most_recent = df['snapshot'].max()
print("Most recent snapshot:", most_recent)

date_today = date.today().isoformat()

if date_today == most_recent.strftime('%Y-%m-%d'):
    print("Data is already up to date.")
    exit(0)