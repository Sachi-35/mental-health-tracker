from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from db import execute_query

admin_routes = Blueprint('admin_routes', __name__)

# Middleware to check if the user is an admin
def is_admin(user_id):
    query = "SELECT role FROM users WHERE id = %s"
    user = execute_query(query, (user_id,), fetchone=True)
    return user and user['role'] == 'admin'

# Fetch all registered users
@admin_routes.route('/admin/users', methods=['GET'])
@jwt_required()
def get_all_users():
    user_id = get_jwt_identity()
    if not is_admin(user_id):
        return jsonify({"error": "Unauthorized access"}), 403
    
    query = "SELECT id, username, email, role, created_at FROM users"
    users = execute_query(query)
    return jsonify(users), 200

# Fetch all mood entries across users
@admin_routes.route('/admin/moods', methods=['GET'])
@jwt_required()
def get_all_moods():
    user_id = get_jwt_identity()
    if not is_admin(user_id):
        return jsonify({"error": "Unauthorized access"}), 403
    
    query = "SELECT user_id, mood_score, sentiment, timestamp FROM mood_entries ORDER BY timestamp DESC"
    moods = execute_query(query)
    return jsonify(moods), 200

# Delete a user by ID
@admin_routes.route('/admin/delete_user/<int:user_id>', methods=['DELETE'])
@jwt_required()
def delete_user(user_id):
    admin_id = get_jwt_identity()
    if not is_admin(admin_id):
        return jsonify({"error": "Unauthorized access"}), 403
    
    delete_query = "DELETE FROM users WHERE id = %s"
    execute_query(delete_query, (user_id,))
    return jsonify({"message": "User deleted successfully"}), 200
