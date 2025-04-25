from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize Flask app
app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

@app.route('/signup', methods=['POST'])
def signup():
    data = request.get_json()
    
    # Validate input
    if not data or 'username' not in data or 'password' not in data:
        return jsonify({'message': 'Missing username or password'}), 400
    
    username = data['username']
    password = data['password']
    
    print(username, password)
    # Create new user
    try:
        # add user to the database
        return jsonify({'message': 'User created successfully'}), 201
    except Exception as e:
        # Any error
        return jsonify({'message': 'Error creating user'}), 500
    
@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    
    # Validate input
    if not data or 'username' not in data or 'password' not in data:
        return jsonify({'message': 'Missing username or password'}), 400
    
    username = data['username']
    password = data['password']
    
    print(username, password)
    # Check if we have the user
    try:
        # check db
        return jsonify({'message': 'Log in successful'}), 201
    except Exception as e:
        return jsonify({'message': 'Error logging in'}), 500
    
@app.route('/search', methods=['POST'])
def search():
    data = request.get_json()
    
    if not data or 'query' not in data:
        return jsonify({'message': 'Missing search query'}), 400
    
    search_query = data['query']
    print(f"Received search query: {search_query}")
    
    return jsonify({
        'message': 'Search query received',
        'query': search_query
    }), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)