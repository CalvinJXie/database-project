import yfinance as yf
import pandas as pd
import time
import csv

# URL of the Wikipedia page containing the S&P 500 companies list.
url = "https://en.wikipedia.org/wiki/List_of_S%26P_500_companies"

# Read all tables from the page.
tables = pd.read_html(url)

# Typically, the first table is the S&P 500 companies list.
sp500_df = tables[0]

# Extract the 'Symbol' column and convert it to a list.
tickers = sp500_df["Symbol"].tolist()

# Print the list of symbols.

headers = ["ticker", "company_name", "sector", "exchange"]

data_list = []

for t in tickers:
    print(f"Retrieving info for {t}...")
    try:
        info = yf.Ticker(t).info
    except Exception as e:
        print(f"Error retrieving info for {t}: {e}")
        continue

    # Create a row dictionary using only our desired fields.
    # For company_name, try "longName" first; if not available, fallback to "shortName".
    company_name = info.get("longName") or info.get("shortName") or ""
    sector = info.get("sector", "")
    # The "exchange" field may not always be present; you might try "fullExchangeName" if needed.
    exchange = info.get("exchange") or info.get("fullExchangeName") or ""

    # Build the row.
    row = {
        "ticker": t,
        "company_name": company_name,
        "sector": sector,
        "exchange": exchange
    }
    data_list.append(row)
    

# Define output CSV file path.
csv_output_path = "stock_info.csv"

# Write the data to CSV.
with open(csv_output_path, "w", newline="", encoding="utf-8") as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=headers)
    writer.writeheader()  # write the header row
    for row in data_list:
        writer.writerow(row)

print(f"CSV file '{csv_output_path}' created successfully.")