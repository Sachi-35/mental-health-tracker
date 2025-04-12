from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token
from datetime import datetime
from app.extensions import db
from sqlalchemy import Column, Integer, String, DateTime


class User(db.Model):
    __tablename__ = 'users'  # This table should match the table name in your MySQL database

    id = Column(Integer, primary_key=True)
    username = Column(String(80), unique=True, nullable=False)  # Username field with unique constraint
    email = Column(String(120), unique=True, nullable=False)  # Email field with unique constraint
    password_hash = Column(String(365), nullable=False)  # Stores hashed password
    created_at = Column(DateTime, default=datetime.utcnow)  # Timestamp when the user was created

    def __init__(self, username, email, password):
        """
        Constructor to initialize the user object with username, email, and password.
        The password is hashed before storing.
        """
        self.username = username
        self.email = email
        self.password_hash = generate_password_hash(password)  # Password is hashed when setting

    def check_password(self, password):
        """
        Compares the provided password with the hashed password stored in the database.
        """
        return check_password_hash(self.password_hash, password)

    def generate_token(self):
        """
        Generates a JWT token for the authenticated user, using their ID as identity.
        """
        return create_access_token(identity=self.id)

    def to_dict(self):
        """
        Converts the User object to a dictionary format, useful for API responses.
        """
        return {
            "id": self.id,
            "username": self.username,
            "email": self.email,
            "created_at": self.created_at.isoformat()  # Converts datetime to ISO format string
        }
