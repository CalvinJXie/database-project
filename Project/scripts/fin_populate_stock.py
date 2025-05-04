import csv
import mysql.connector

def populate_stock_table_from_csv(csv_file_path):
    try:
        # Connect to the MySQL database.
        conn = mysql.connector.connect(
            host="localhost",
            user="root",             # Replace if you're using a different user.
            password="Hello123#",    # Replace with your actual password.
            database="MoneyMaker"    # Your database name.
        )
        cursor = conn.cursor()
        print("Connected to the database successfully.")
    except mysql.connector.Error as err:
        print("Error connecting to the database:", err)
        return

    # Open the CSV file and read its contents.
    try:
        with open(csv_file_path, mode='r', newline='', encoding='utf-8') as file:
            # Assume the CSV file has a header row with these column names: 
            # "ticker", "company_name", "sector", "exchange"
            reader = csv.DictReader(file)
            row_count = 0
            for row in reader:
                ticker = row.get("ticker", "").strip()
                company_name = row.get("company_name", "").strip()
                sector = row.get("sector", "").strip()
                exchange = row.get("exchange", "").strip()

                # Prepare the INSERT query; note we do not include stock_id.
                insert_query = """
                    INSERT INTO Stock (company_name, ticker, sector, exchange)
                    VALUES (%s, %s, %s, %s);
                """
                values = (company_name, ticker, sector, exchange)
                
                try:
                    cursor.execute(insert_query, values)
                    row_count += 1
                except mysql.connector.Error as err:
                    print(f"Error inserting {ticker}: {err}")
                    
            # Commit all the inserts.
            conn.commit()
            print(f"{row_count} rows inserted into the Stock table.")
    except FileNotFoundError:
        print(f"CSV file '{csv_file_path}' not found.")
    except Exception as e:
        print("Error reading CSV file:", e)
    finally:
        cursor.close()
        conn.close()

if __name__ == "__main__":
    # Path to your CSV file generated previously (e.g. from the S&P 500 companies list)
    csv_file_path = "sp500_companies.csv"
    populate_stock_table_from_csv(csv_file_path)
