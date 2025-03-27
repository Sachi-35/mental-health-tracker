from datetime import timedelta
from flask import Flask, jsonify
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_jwt_extended import JWTManager
from flask_cors import CORS
import mysql.connector

from routes.user_routes import user_routes
from routes.auth_routes import auth_routes
from routes.sentiment import sentiment_bp
from routes.mood_routes import mood_routes
from routes.admin_routes import admin_routes

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}}, supports_credentials=True)

limiter = Limiter(get_remote_address, app=app, default_limits=["5 per minute"])

jwt = JWTManager(app)
app.config['JWT_SECRET_KEY'] = 'secure_password_2025'
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=1)

@jwt.unauthorized_loader
def unauthorized_callback(callback):
    return jsonify({"error": "Missing or invalid token"}), 401

@jwt.invalid_token_loader
def invalid_token_callback(callback):
    return jsonify({"error": "Invalid token"}), 422

@jwt.expired_token_loader
def expired_token_callback(jwt_header, jwt_payload):
    return jsonify({"msg": "Token has expired"}), 401

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'  
app.config['MYSQL_PASSWORD'] = 'sachi2005'  
app.config['MYSQL_DATABASE'] = 'mental_health_tracker'

def get_db_connection():
    return mysql.connector.connect(
        host=app.config['MYSQL_HOST'],
        user=app.config['MYSQL_USER'],
        password=app.config['MYSQL_PASSWORD'],
        database=app.config['MYSQL_DATABASE']
    )

app.register_blueprint(user_routes, url_prefix="/users")
app.register_blueprint(auth_routes, url_prefix="/auth")
app.register_blueprint(sentiment_bp, url_prefix="/sentiment")
app.register_blueprint(mood_routes, url_prefix="/mood")
app.register_blueprint(admin_routes, url_prefix='/admin')

@app.route("/")
def home():
    return jsonify({"message": "Mental Health Tracker API is running!"})

if __name__ == "__main__":
    app.run(debug=True, port=5001)
