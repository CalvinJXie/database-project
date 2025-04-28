from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import os
from dotenv import load_dotenv
from datetime import datetime
from decimal import Decimal

app = Flask(__name__)

# Load environment variables
load_dotenv()
#-----
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)


#-----

# Initialize Flask app
CORS(app, resources={r"/*": {"origins": "*"}})

@app.route('/signup', methods=['POST'])
def signup():
    data = request.get_json()

    if not data or 'username' not in data or 'password' not in data:
        return jsonify({'message': 'Missing username or password'}), 400

    username = data['username']
    password = data['password']

    print(f"Signup attempt: username={username}, password={password}")

    try:
        conn = db.engine.raw_connection()
        cursor = conn.cursor()

        check_query = f"SELECT * FROM users WHERE username = '{username}';"
        cursor.execute(check_query)
        existing_user = cursor.fetchone()

        if existing_user:
            return jsonify({'message': 'Username already exists'}), 409

        # Insert new user
        insert_query = f"INSERT INTO users (username, password) VALUES ('{username}', '{password}');"
        cursor.execute(insert_query)

        cursor.execute("SELECT LAST_INSERT_ID();")
        user_id = cursor.fetchone()[0]

        conn.commit()

        return jsonify({
            'message': 'User created successfully',
            'userId': user_id
        }), 201
    except Exception as e:
        print(f"Error during signup: {e}")
        return jsonify({'message': 'Error creating user'}), 500



@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    
    if not data or 'username' not in data or 'password' not in data:
        return jsonify({'message': 'Missing username or password'}), 400
    
    username = data['username']
    password = data['password']
    
    print(username, password)

    try:
        query = f"SELECT user_id FROM Users WHERE username = '{username}' AND password = '{password}';"
        
        cursor = db.engine.raw_connection().cursor()
        cursor.execute(query)
        result = cursor.fetchone()
        
        if result:
            user_id = result[0]  # get the ID from the query result
            return jsonify({
                'message': 'Log in successful',
                'userId': user_id
            }), 200
        else:
            return jsonify({'message': 'Invalid credentials'}), 401

    except Exception as e:
        print(f"Error during login: {e}")
        return jsonify({'message': 'Error logging in'}), 500

    
@app.route('/search_stock', methods=['POST'])
def search_stock():
    data = request.get_json()

    if not data or 'ticker' not in data:
        return jsonify({'message': 'Missing ticker symbol'}), 400

    ticker = data['ticker'].upper()

    try:
        conn = db.engine.raw_connection()
        cursor = conn.cursor()

        query = """
        SELECT s.company_name, s.ticker, s.sector, s.exchange, d.current_price, d.volume, d.data_time
        FROM Stock s
        JOIN Stock_Data d ON s.stock_id = d.stock_id
        WHERE s.ticker = %s
        ORDER BY d.data_time DESC
        LIMIT 1;
        """
        cursor.execute(query, (ticker,))
        result = cursor.fetchone()

        if result:
            stock_info = {
                'company_name': result[0],
                'ticker': result[1],
                'sector': result[2],
                'exchange': result[3],
                'price': float(result[4]),
                'volume': result[5],
                'data_time': result[6].strftime('%Y-%m-%d %H:%M:%S') if result[6] else None
            }
            return jsonify({'stock': stock_info}), 200
        else:
            return jsonify({'message': 'Stock not found'}), 404

    except Exception as e:
        print(f"Error searching for stock: {e}")
        return jsonify({'message': 'Error searching for stock'}), 500



@app.route('/transactions', methods=['POST'])
def transactions():
    data = request.get_json()

    if not data or 'user_id' not in data:
        return jsonify({'message': 'Missing user_id'}), 400

    user_id = data['user_id']

    try:
        conn = db.engine.raw_connection()
        cursor = conn.cursor()

        query = """
        SELECT t.transaction_id, s.ticker, t.price, t.quantity, t.transaction_type, t.transaction_time
        FROM Transaction t
        JOIN Stock s ON t.stock_id = s.stock_id
        WHERE t.user_id = %s
        ORDER BY t.transaction_time DESC
        """
        cursor.execute(query, (user_id,))
        results = cursor.fetchall()

        transactions = []
        for row in results:
            transactions.append({
                'id': row[0],
                'stock': row[1],
                'price': float(row[2]),
                'quantity': row[3],
                'type': row[4],
                'time': row[5].strftime('%Y-%m-%d %H:%M:%S')
            })

        return jsonify({'transactions': transactions}), 200

    except Exception as e:
        print(f"Error fetching transactions: {e}")
        return jsonify({'message': 'Error fetching transactions'}), 500
    
@app.route('/portfolio', methods=['POST'])
def portfolio():
    data = request.get_json()

    if not data or 'user_id' not in data:
        return jsonify({'message': 'Missing user_id'}), 400

    user_id = data['user_id']

    try:
        conn = db.engine.raw_connection()
        cursor = conn.cursor()

        # Get user's current balance
        query_balance = """
        SELECT balance
        FROM Portfolio
        WHERE user_id = %s;
        """
        cursor.execute(query_balance, (user_id,))
        balance_result = cursor.fetchone()

        if not balance_result:
            return jsonify({'message': 'User not found or no portfolio data'}), 404

        balance = float(balance_result[0])

        # Get all transactions for the user, including both buys and sells
        query_transactions = """
        SELECT s.ticker, t.transaction_type, t.quantity, s.stock_id
        FROM Transaction t
        JOIN Stock s ON t.stock_id = s.stock_id
        WHERE t.user_id = %s
        """
        cursor.execute(query_transactions, (user_id,))
        transaction_results = cursor.fetchall()

        portfolio = {}
        total_investments = 0

        # Track active holdings (only add stocks that have a positive quantity)
        for row in transaction_results:
            ticker = row[0]
            transaction_type = row[1]
            quantity = row[2]
            stock_id = row[3]

            # Initialize the stock if not already present in the portfolio
            if ticker not in portfolio:
                portfolio[ticker] = 0

            # Update the portfolio based on transaction type (buy or sell)
            if transaction_type == 'BUY':
                portfolio[ticker] += quantity
            elif transaction_type == 'SELL':
                portfolio[ticker] -= quantity

        # Remove any stocks with zero or negative quantity
        active_portfolio = {ticker: quantity for ticker, quantity in portfolio.items() if quantity > 0}

        # For each active stock, calculate the current value using the most recent price
        active_holdings = []
        for ticker, quantity in active_portfolio.items():
            # Fetch the most recent price for each stock
            query_current_price = """
            SELECT current_price
            FROM Stock_Data
            WHERE stock_id = (SELECT stock_id FROM Stock WHERE ticker = %s)
            ORDER BY data_time DESC LIMIT 1;
            """
            cursor.execute(query_current_price, (ticker,))
            price_result = cursor.fetchone()

            if price_result:
                current_price = float(price_result[0])
                total_value = quantity * current_price
                total_investments += total_value

                active_holdings.append({
                    'ticker': ticker,
                    'quantity': quantity,  # Add quantity to the response data
                    'total_value': total_value,
                    'current_price': current_price
                })

        return jsonify({
            'portfolio': active_holdings,
            'total_investments': total_investments,
            'balance': balance
        }), 200

    except Exception as e:
        print(f"Error fetching portfolio: {e}")
        return jsonify({'message': 'Error fetching portfolio'}), 500
    
@app.route('/buy_stock', methods=['POST'])
def buy_stock():
    data = request.get_json()

    if not data or 'user_id' not in data or 'ticker' not in data or 'quantity' not in data:
        return jsonify({'message': 'Missing required fields'}), 400

    user_id = data['user_id']
    ticker = data['ticker']
    quantity = int(data['quantity'])

    # Ensure quantity is a positive number
    if quantity <= 0:
        return jsonify({'message': 'Quantity must be greater than zero'}), 400

    try:
        cursor = db.engine.raw_connection().cursor()

        # Get the stock price for the ticker
        cursor.execute("""
            SELECT Stock_Data.current_price, Stock.stock_id 
            FROM Stock
            JOIN Stock_Data ON Stock.stock_id = Stock_Data.stock_id
            WHERE Stock.ticker = %s
            ORDER BY Stock_Data.data_time DESC LIMIT 1
        """, (ticker,))
        stock = cursor.fetchone()

        if not stock:
            return jsonify({'message': 'Stock not found'}), 404

        current_price = stock[0]
        stock_id = stock[1]

        # Calculate the total price of the transaction
        total_price = Decimal(current_price) * Decimal(quantity)  # Ensure total_price is Decimal

        # Get user's balance
        cursor.execute("""
            SELECT balance FROM Portfolio WHERE user_id = %s
        """, (user_id,))
        balance = cursor.fetchone()

        if not balance:
            return jsonify({'message': 'User not found'}), 404

        balance = Decimal(balance[0])  # Convert balance to Decimal

        # Check if the user has enough balance to buy the stock
        if balance < total_price:
            return jsonify({'message': 'Insufficient balance'}), 400

        # Deduct balance
        new_balance = balance - total_price
        cursor.execute("""
            UPDATE Portfolio SET balance = %s WHERE user_id = %s
        """, (new_balance, user_id))

        # Add the stock purchase to the transaction table
        cursor.execute("""
            INSERT INTO Transaction (user_id, stock_id, price, quantity, transaction_type, transaction_time)
            VALUES (%s, %s, %s, %s, 'BUY', NOW())
        """, (user_id, stock_id, current_price, quantity))

        print(f"User {user_id} bought {quantity} shares of {ticker} at {current_price} each.")
        # Commit the transaction manually after the raw SQL operations
        cursor.connection.commit()

        db.session.commit()
        return jsonify({'message': 'Purchase successful'}), 200

    except Exception as e:
        db.session.rollback()  # Rollback any changes if an error occurs
        print(f"Error during purchase: {str(e)}")  # Log the error message to the console
        return jsonify({'message': 'An error occurred while processing your request'}), 500



@app.route('/sell_stock', methods=['POST'])
def sell_stock():
    data = request.get_json()

    if not data or 'user_id' not in data or 'ticker' not in data or 'quantity' not in data:
        return jsonify({'message': 'Missing required fields'}), 400

    user_id = data['user_id']
    ticker = data['ticker']
    quantity = int(data['quantity'])

    # Ensure quantity is a positive number
    if quantity <= 0:
        return jsonify({'message': 'Quantity must be greater than zero'}), 400

    try:
        cursor = db.engine.raw_connection().cursor()

        # Get the stock price for the ticker
        cursor.execute("""
            SELECT Stock_Data.current_price, Stock.stock_id 
            FROM Stock
            JOIN Stock_Data ON Stock.stock_id = Stock_Data.stock_id
            WHERE Stock.ticker = %s
            ORDER BY Stock_Data.data_time DESC LIMIT 1
        """, (ticker,))
        stock = cursor.fetchone()

        if not stock:
            return jsonify({'message': 'Stock not found'}), 404

        current_price = stock[0]
        stock_id = stock[1]

        # Get user's holdings for the stock (bought quantity)
        cursor.execute("""
            SELECT SUM(quantity) 
            FROM Transaction 
            WHERE user_id = %s AND stock_id = %s AND transaction_type = 'BUY'
        """, (user_id, stock_id))
        bought_quantity = cursor.fetchone()[0] or 0

        # Get the quantity of shares sold by the user (sold quantity)
        cursor.execute("""
            SELECT SUM(quantity) 
            FROM Transaction 
            WHERE user_id = %s AND stock_id = %s AND transaction_type = 'SELL'
        """, (user_id, stock_id))
        sold_quantity = cursor.fetchone()[0] or 0

        # Calculate the current quantity the user owns
        current_quantity = bought_quantity - sold_quantity

        # Ensure the user has enough shares to sell
        if current_quantity < quantity:
            return jsonify({'message': 'Insufficient shares to sell'}), 400

        # Add the stock sale to the transaction table
        cursor.execute("""
            INSERT INTO Transaction (user_id, stock_id, price, quantity, transaction_type, transaction_time)
            VALUES (%s, %s, %s, %s, 'SELL', NOW())
        """, (user_id, stock_id, current_price, quantity))

        # Add the proceeds from the sale to the user's balance
        total_proceeds = current_price * quantity
        cursor.execute("""
            UPDATE Portfolio SET balance = balance + %s WHERE user_id = %s
        """, (total_proceeds, user_id))

        # Commit the transaction manually after the raw SQL operations
        cursor.connection.commit()

        return jsonify({'message': 'Sale successful'}), 200

    except Exception as e:
        db.session.rollback()  # Rollback any changes if an error occurs
        print(f"Error during sale: {str(e)}")  # Log the error message to the console
        return jsonify({'message': 'An error occurred while processing your request'}), 500



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)
