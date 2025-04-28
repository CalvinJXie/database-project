import yfinance as yf
import mysql.connector
import csv
from datetime import datetime
import schedule
import time


def get_stock_mapping_from_db():
    mapping = {}
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="Hello123#",
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
    stock_mapping = get_stock_mapping_from_db()
    if not stock_mapping:
        print("No stock mapping found. Cannot update data.")
        return

    csv_file = "data/sp500_companies.csv"
    csv_tickers = get_tickers_from_csv(csv_file)
    if not csv_tickers:
        print(f"No tickers found in {csv_file}.")
        return

    print(f"Updating data for tickers: {csv_tickers}")
    
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

    for ticker_symbol in csv_tickers:
        try:
            data = yf.download(ticker_symbol, period="1d", interval="1m", progress=False)
            if data.empty:
                print(f"No data retrieved for {ticker_symbol}.")
                continue

            latest_data = data.iloc[-1]
            data_time = latest_data.name.strftime("%Y-%m-%d %H:%M:%S")

            # Fix the FutureWarning by using .iloc[0]
            open_price = float(latest_data['Open'].iloc[0])
            high_price = float(latest_data['High'].iloc[0])
            low_price = float(latest_data['Low'].iloc[0])
            close_price = float(latest_data['Close'].iloc[0])
            volume = int(latest_data['Volume'].iloc[0])
            current_price = close_price

            stock_id = stock_mapping.get(ticker_symbol)
            if not stock_id:
                print(f"No stock_id mapping for {ticker_symbol}. Skipping update for this ticker.")
                continue

            check_query = "SELECT COUNT(*) FROM Stock_Data WHERE stock_id = %s"
            cursor.execute(check_query, (stock_id,))
            record_exists = cursor.fetchone()[0] > 0

            if record_exists:
                update_query = """
                    UPDATE Stock_Data 
                    SET current_price = %s, open_price = %s, close_price = %s, 
                        low_price = %s, high_price = %s, volume = %s, data_time = %s
                    WHERE stock_id = %s
                """
                values = (current_price, open_price, close_price, low_price, high_price, volume, data_time, stock_id)
                cursor.execute(update_query, values)
                print(f"Data updated for {ticker_symbol} at {data_time}: {current_price}")
            else:
                insert_query = """
                    INSERT INTO Stock_Data 
                    (stock_id, current_price, open_price, close_price, low_price, high_price, volume, data_time)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                """
                values = (stock_id, current_price, open_price, close_price, low_price, high_price, volume, data_time)
                cursor.execute(insert_query, values)
                print(f"New data inserted for {ticker_symbol} at {data_time}: {current_price}")
            
            conn.commit()
        except Exception as e:
            print(f"Error processing {ticker_symbol}: {e}")

    cursor.close()
    conn.close()

# Schedule the update_stock_data function to run every 30 seconds.
schedule.every(30).seconds.do(update_stock_data)

print("Starting the stock data update process using CSV tickers...")
while True:
    schedule.run_pending()
    time.sleep(1)