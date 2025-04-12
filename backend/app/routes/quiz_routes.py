from flask import Blueprint, request, jsonify
from app.models.user import User
from app.extensions import db
from datetime import datetime

quiz_bp = Blueprint('quiz', __name__)

@quiz_bp.route("/submit_quiz", methods=["POST"])
def submit_quiz():
    data = request.json
    user_id = data.get("user_id")
    question = data.get("question")
    answer = data.get("answer")

    if not user_id or not question or not answer:
        return jsonify({"error": "Missing data"}), 400

    # Insert into quiz_responses table manually
    try:
        query = """
            INSERT INTO quiz_responses (user_id, question, answer, timestamp)
            VALUES (%s, %s, %s, %s)
        """
        db.session.execute(query, (user_id, question, answer, datetime.utcnow()))
        db.session.commit()
        return jsonify({"message": "Quiz response submitted successfully"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500
