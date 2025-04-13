from flask import Blueprint, request, jsonify
from app.models.quiz_response import QuizResponse  # Assuming you have a model for quiz responses
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

    # Using SQLAlchemy ORM to insert the response
    try:
        quiz_response = QuizResponse(
            user_id=user_id,
            question=question,
            answer=answer,
            timestamp=datetime.utcnow()
        )
        db.session.add(quiz_response)
        db.session.commit()
        return jsonify({"message": "Quiz response submitted successfully"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500
