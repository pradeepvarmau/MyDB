'''from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
import os

app = Flask(__name__)

# PostgreSQL configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://username:password@localhost:5432/your_database'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(10), default='user')


class Data(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    country = db.Column(db.String(100))
    state = db.Column(db.String(100))
    industry = db.Column(db.String(100))
    sub_industry = db.Column(db.String(100))
    city = db.Column(db.String(100))

@app.route('/api/signup', methods=['POST'])
def signup():
    data = request.get_json()
    new_user = User(
        username=data['username'],
        email=data['email'],
        password_hash=generate_password_hash(data['password'])
    )
    db.session.add(new_user)
    db.session.commit()
    return jsonify({"message": "User created successfully!"}), 201

@app.route('/api/login', methods=['POST'])
def login():
    data = request.get_json()
    user = User.query.filter_by(username=data['username']).first()
    if user and check_password_hash(user.password_hash, data['password']):
        return jsonify({"message": "Login successful!"}), 200
    return jsonify({"message": "Invalid credentials!"}), 401

@app.route('/api/upload', methods=['POST'])
def upload_data():
    data = request.get_json()
    new_data = Data(
        country=data['country'],
        state=data['state'],
        industry=data['industry'],
        sub_industry=data['sub_industry'],
        city=data['city']
    )
    db.session.add(new_data)
    db.session.commit()
    return jsonify({"message": "Data uploaded successfully!"}), 201


@app.route('/api/filter', methods=['GET'])
def filter_data():
    country = request.args.get('country')
    state = request.args.get('state')
    industry = request.args.get('industry')
    sub_industry = request.args.get('sub_industry')
    city = request.args.get('city')
    
    query = Data.query
    
    if country:
        query = query.filter(Data.country == country)
    if state:
        query = query.filter(Data.state == state)
    if industry:
        query = query.filter(Data.industry == industry)
    if sub_industry:
        query = query.filter(Data.sub_industry == sub_industry)
    if city:
        query = query.filter(Data.city == city)

    results = query.all()
    return jsonify([{"id": d.id, "country": d.country, "state": d.state, "industry": d.industry,
                     "sub_industry": d.sub_industry, "city": d.city} for d in results]), 200

if __name__ == '__main__':
    db.create_all()  # Create tables
    app.run(debug=True)'''

from flask import Flask, request, jsonify
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)

# SQLite database configuration
DATABASE = 'your_database.db'

def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/api/signup', methods=['POST'])
def signup():
    data = request.get_json()
    password_hash = generate_password_hash(data['password'])

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('INSERT INTO users (username, email, password_hash) VALUES (?, ?, ?)',
                   (data['username'], data['email'], password_hash))
    conn.commit()
    conn.close()

    return jsonify({"message": "User created successfully!"}), 201

@app.route('/api/login', methods=['POST'])
def login():
    data = request.get_json()
    conn = get_db_connection()
    user = conn.execute('SELECT * FROM users WHERE username = ?', (data['username'],)).fetchone()
    conn.close()

    if user and check_password_hash(user['password_hash'], data['password']):
        return jsonify({"message": "Login successful!"}), 200
    return jsonify({"message": "Invalid credentials!"}), 401

@app.route('/api/upload', methods=['POST'])
def upload_data():
    data = request.get_json()

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('INSERT INTO data (country, state, industry, sub_industry, city) VALUES (?, ?, ?, ?, ?)',
                   (data['country'], data['state'], data['industry'], data['sub_industry'], data['city']))
    conn.commit()
    conn.close()

    return jsonify({"message": "Data uploaded successfully!"}), 201

@app.route('/api/filter', methods=['GET'])
def filter_data():
    country = request.args.get('country')
    state = request.args.get('state')
    industry = request.args.get('industry')
    sub_industry = request.args.get('sub_industry')
    city = request.args.get('city')

    query = 'SELECT * FROM data WHERE 1=1'
    params = []

    if country:
        query += ' AND country = ?'
        params.append(country)
    if state:
        query += ' AND state = ?'
        params.append(state)
    if industry:
        query += ' AND industry = ?'
        params.append(industry)
    if sub_industry:
        query += ' AND sub_industry = ?'
        params.append(sub_industry)
    if city:
        query += ' AND city = ?'
        params.append(city)

    conn = get_db_connection()
    results = conn.execute(query, params).fetchall()
    conn.close()

    return jsonify([{"id": d['id'], "country": d['country'], "state": d['state'], 
                     "industry": d['industry'], "sub_industry": d['sub_industry'], "city": d['city']} 
                     for d in results]), 200

if __name__ == '__main__':
    # Create database and tables
    conn = get_db_connection()
    conn.execute('CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT UNIQUE, email TEXT UNIQUE, password_hash TEXT)')
    conn.execute('CREATE TABLE IF NOT EXISTS data (id INTEGER PRIMARY KEY AUTOINCREMENT, country TEXT, state TEXT, industry TEXT, sub_industry TEXT, city TEXT)')
    conn.close()

    app.run(debug=True)
