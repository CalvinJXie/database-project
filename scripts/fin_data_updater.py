import yfinance as yf
import mysql.connector
import csv
import schedule
import time
from datetime import datetime

def get_stock_mapping_from_db():
    """
    Connect to the database and retrieve the mapping of ticker to stock_id.
    The function returns a dictionary with ticker symbols (uppercased) as keys
    and corresponding stock_id values.
    """
    mapping = {}
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="Hello123#",  # Replace with your actual password.
            database="MoneyMaker"
        )
        cursor = conn.cursor()
        cursor.execute("SELECT stock_id, ticker FROM Stock")
        for stock_id, ticker in cursor.fetchall():
            mapping[ticker.upper()] = stock_id
        cursor.close()
        conn.close()
    except mysql.connector.Error as err:
        print("Error querying database for stock mapping:", err)
    return mapping

def get_tickers_from_csv(csv_file_path):
    """
    Reads the provided CSV file and returns a list of ticker symbols.
    Assumes the CSV file contains a header with at least a 'ticker' column.
    """
    tickers = []
    try:
        with open(csv_file_path, mode="r", newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                ticker = row.get("ticker", "").strip()
                if ticker:
                    tickers.append(ticker.upper())
    except Exception as e:
        print(f"Error reading CSV file '{csv_file_path}':", e)
    return tickers

def update_stock_data():
    # First, retrieve our ticker-to-stock_id mapping from the Stock table.
    stock_mapping = get_stock_mapping_from_db()
    if not stock_mapping:
        print("No stock mapping found. Cannot update data.")
        return

    # Get the list of tickers from the CSV.
    csv_file = "sp500_companies.csv"  # Adjust this to the correct path if needed.
    csv_tickers = get_tickers_from_csv(csv_file)
    if not csv_tickers:
        print(f"No tickers found in {csv_file}.")
        return

    print(f"Updating data for tickers: {csv_tickers}")
    
    # Connect to the MySQL database.
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="Hello123#",
            database="MoneyMaker"
        )
        cursor = conn.cursor()
    except Exception as e:
        print("Error connecting to the database:", e)
        return

    # For each ticker from the CSV, retrieve the latest market data and insert into Stock_Data.
    for ticker_symbol in csv_tickers:
        try:
            # Retrieve the most recent 1-day data at a 1-minute interval using yfinance.
            data = yf.download(ticker_symbol, period="1d", interval="1m", progress=False)
            if data.empty:
                print(f"No data retrieved for {ticker_symbol}.")
                continue

            # Get the latest row of data.
            latest_data = data.iloc[-1]
            data_time = latest_data.name.strftime("%Y-%m-%d %H:%M:%S")

            # Convert each value to appropriate native Python types.
            open_price = float(latest_data['Open'])
            high_price = float(latest_data['High'])
            low_price = float(latest_data['Low'])
            close_price = float(latest_data['Close'])
            volume = int(latest_data['Volume'])
            current_price = close_price  # Using the close price as current price.

            # Lookup the stock_id from the database mapping.
            stock_id = stock_mapping.get(ticker_symbol)
            if not stock_id:
                print(f"No stock_id mapping for {ticker_symbol}. Skipping update for this ticker.")
                continue

            # Prepare the INSERT query for the Stock_Data table.
            insert_query = """
                INSERT INTO Stock_Data 
                (stock_id, current_price, open_price, close_price, low_price, high_price, volume, data_time)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """
            values = (stock_id, current_price, open_price, close_price, low_price, high_price, volume, data_time)
            cursor.execute(insert_query, values)
            conn.commit()
            print(f"Data updated for {ticker_symbol} at {data_time}: {current_price}")
        except Exception as e:
            print(f"Error processing {ticker_symbol}: {e}")

    cursor.close()
    conn.close()

# Schedule the update_stock_data function to run every 30 seconds.
# schedule.every(30).seconds.do(update_stock_data)

# print("Starting the stock data update process using CSV tickers...")
# while True:
#     schedule.run_pending()
#     time.sleep(1)

update_stock_data()