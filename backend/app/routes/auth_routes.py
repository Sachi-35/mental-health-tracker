from flask import Blueprint, request, jsonify
from flask import current_app
from flask_jwt_extended import create_access_token
from app.models.user import User
from app.extensions import db
from sqlalchemy.exc import IntegrityError
from werkzeug.security import generate_password_hash, check_password_hash
import datetime

auth_bp = Blueprint('auth', __name__, url_prefix='/api/auth')

# Signup route
@auth_bp.route('/signup', methods=['POST'])
def signup():
    data = request.get_json()
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')

    if not username or not email or not password:
        return jsonify({"message": "Missing fields"}), 400

    user = User(username=username, email=email, password=password)

    try:
        db.session.add(user)
        db.session.commit()
        return jsonify({"message": "User registered successfully"}), 201
    except IntegrityError:
        db.session.rollback()
        return jsonify({"message": "Username or email already exists"}), 409

# Login route
@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    user = User.query.filter_by(email=email).first()

    if user and check_password_hash(user.password_hash, password):
        # Use create_access_token for easier JWT generation
        token = create_access_token(identity=user.id)
        return jsonify({'token': token, 'user': {'id': user.id, 'username': user.username, 'email': user.email}})
    else:
        return jsonify({'message': 'Invalid email or password'}), 401
