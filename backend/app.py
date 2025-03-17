from flask import Flask
import mysql.connector
from flask_jwt_extended import JWTManager
from routes.user_routes import user_routes
from routes.auth_routes import auth_routes

app = Flask(__name__)

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

# JWT Configuration
app.config['JWT_SECRET_KEY'] = 'your_secret_key'  # Change this to a strong secret key
jwt = JWTManager(app)

# Register Blueprints (Routes)
app.register_blueprint(user_routes, url_prefix="/users")
app.register_blueprint(auth_routes, url_prefix="/auth")

@app.route("/")
def home():
    return {"message": "Mental Health Tracker API is running!"}

if __name__ == "__main__":
    app.run(debug=True)
