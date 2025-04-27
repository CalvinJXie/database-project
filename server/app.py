from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
#-----
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)


#-----

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
        #----
        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            return jsonify({'message': 'Username already exists'}), 409
    
        new_user = User(username=username, password=password)
        db.session.add(new_user)
        db.session.commit()
        
        #----
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

        #BAD QUERY FOR SQL INJECTION part A
        query = f"SELECT * FROM Users WHERE username = '{username}' AND password = '{password}';"
        
        cursor = db.engine.raw_connection().cursor()
        cursor.execute(query)
        result = cursor.fetchone()
        
        if result:
            return jsonify({'message': 'Log in successful'}), 200
        else:
            return jsonify({'message': 'Invalid credentials'}), 401

        #ORIGINAL QUERY
        #---------
        # user = User.query.filter_by(username=username, password=password).first()
        # if user:
        #     return jsonify({'message': 'Log in successful'}), 200
        # else:
        #     return jsonify({'message': 'Invalid username or password'}), 401
        #---------
        # check db
        #return jsonify({'message': 'Log in successful'}), 201
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
