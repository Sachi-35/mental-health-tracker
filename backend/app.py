from flask import Flask
import mysql.connector
from flask_jwt_extended import JWTManager
from routes.user_routes import user_routes
from routes.auth_routes import auth_routes
from routes.sentiment import sentiment_bp
from flask_jwt_extended import JWTManager
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
app.config['JWT_SECRET_KEY'] = 'secure_password_2025'  # Use a secure, secret key!
jwt = JWTManager(app)

# Database Configuration
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'  
app.config['MYSQL_PASSWORD'] = 'sachi2005'  # Change to your MySQL password
app.config['MYSQL_DATABASE'] = 'mental_health_tracker'

# Create MySQL connection
def get_db_connection():
    return mysql.connector.connect(
        host=app.config['MYSQL_HOST'],
        user=app.config['MYSQL_USER'],
        password=app.config['MYSQL_PASSWORD'],
        database=app.config['MYSQL_DATABASE']
    )

from routes.mood_routes import mood_routes

# Register Blueprints (Routes)
app.register_blueprint(user_routes, url_prefix="/users")
app.register_blueprint(auth_routes, url_prefix="/auth")
app.register_blueprint(sentiment_bp, url_prefix="/sentiment")
app.register_blueprint(mood_routes, url_prefix='/mood')

@app.route("/")
def home():
    return {"message": "Mental Health Tracker API is running!"}

if __name__ == "__main__":
    app.run(debug=True)
