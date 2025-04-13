from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from flask_mysqldb import MySQL
from flask_migrate import Migrate
import os
from dotenv import load_dotenv
from .extensions import db
from .models import * 
from .routes import register_routes 

jwt = JWTManager()
mysql = MySQL()
migrate = Migrate()

def create_app():
    app = Flask(__name__)
    load_dotenv()  # Load environment variables

    # Set the configuration from the environment variables
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY')
    
    # Optionally load any other environment variables
    app.config['MYSQL_HOST'] = os.getenv('MYSQL_HOST')
    app.config['MYSQL_USER'] = os.getenv('MYSQL_USER')
    app.config['MYSQL_PASSWORD'] = os.getenv('MYSQL_PASSWORD')
    app.config['MYSQL_DB'] = os.getenv('MYSQL_DB')

    # Load custom config class
    app.config.from_object('config.Config')
    
    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)
    register_routes(app)
    CORS(app)  # Allow cross-origin requests

    # Initialize MySQL (for direct queries if needed)
    mysql.init_app(app)

    return app
