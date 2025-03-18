from flask import Blueprint, request, jsonify, current_app
from flask_jwt_extended import create_access_token
import bcrypt
import mysql.connector

auth_routes = Blueprint('auth_routes', __name__)

# Function to create a new database connection
def get_db_connection():
    return mysql.connector.connect(
        host=current_app.config['MYSQL_HOST'],
        user=current_app.config['MYSQL_USER'],
        password=current_app.config['MYSQL_PASSWORD'],
        database=current_app.config['MYSQL_DATABASE']
    )

@auth_routes.route('/signup', methods=['POST'])
def signup():
    data = request.get_json()
    username = data.get("username")
    email = data.get("email")
    password = data.get("password")

    if not username or not email or not password:
        return jsonify({"error": "All fields are required"}), 400

    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO users (username, email, password) VALUES (%s, %s, %s)",
                       (username, email, hashed_password.decode('utf-8')))
        conn.commit()
        cursor.close()
        conn.close()
        return jsonify({"message": "User registered successfully!"}), 201
    except Exception as e:
        print("Signup Error:", e)  # This will show the error in your terminal
        return jsonify({"error": "Internal server error"}), 500



@auth_routes.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get("email")
    password = data.get("password")

    if not email or not password:
        return jsonify({"error": "All fields are required"}), 400

    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
        user = cursor.fetchone()
        cursor.close()
        conn.close()

        if user and bcrypt.checkpw(password.encode('utf-8'), user["password"].encode('utf-8')):
            access_token = create_access_token(identity=user["id"])
            return jsonify({"access_token": access_token}), 200
        else:
            return jsonify({"error": "Invalid credentials"}), 401

    except Exception as e:
        return jsonify({"error": str(e)}), 500
