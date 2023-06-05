from flask import Flask, jsonify, request
from flask_cors import CORS
import sqlite3
import bcrypt
import jwt
import datetime
import secrets
import base64


app = Flask(__name__)
CORS(app)

app.config['SECRET_KEY'] = secrets.token_hex(16)

@app.route('/api/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data['username']
    email = data['email']
    password = data['password']

    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()

    # check if user already exists
    cursor.execute('SELECT * FROM users WHERE username = ?', (username,))
    user = cursor.fetchone()
    if user:
        return jsonify({'error': 'Username already exists'}), 400

    # hash password
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

    # insert user into database
    cursor.execute('INSERT INTO users (username, email, password) VALUES (?, ?, ?)', (username, email, hashed_password))
    conn.commit()
    conn.close()

    return jsonify({'message': 'User registered successfully'}), 201

@app.route('/api/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data['username']
    password = data['password']

    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()

    # get user from database
    cursor.execute('SELECT * FROM users WHERE username = ?', (username,))
    user = cursor.fetchone()
    conn.close()

    if not user or not bcrypt.checkpw(password.encode('utf-8'), user[3]):
        return jsonify({'error': 'Invalid username or password'}), 401

    # create JWT token
    token = jwt.encode({'user_id': user[0], 'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=1)}, app.config['SECRET_KEY'])

    token_base64 = base64.b64encode(token.encode('utf-8')).decode('utf-8')
    return jsonify({'token': token_base64})


@app.route('/api/user', methods=['GET'])
def get_user():
    token = request.headers.get('Authorization').split()[1]
    try:
        payload = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
        user_id = payload['user_id']
        
        conn = sqlite3.connect('users.db')
        cursor = conn.cursor()
        
        # Truy vấn dữ liệu người dùng từ cơ sở dữ liệu theo user_id
        cursor = conn.execute('SELECT id, username FROM users WHERE id = ?', (user_id,))
        row = cursor.fetchone()
        if row is None:
            return jsonify({'error': 'User not found'}), 404
        user = {'id': row[0], 'username': row[1]}
        return jsonify(user)
    except jwt.ExpiredSignatureError:
        return jsonify({'error': 'Token has expired'}), 401
    except (jwt.InvalidTokenError, Exception) as e:
        return jsonify({'error': 'Invalid token'}), 401
    

if __name__ == '__main__':
    app.run(debug=True)