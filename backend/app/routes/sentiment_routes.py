from flask import Blueprint, request, jsonify
from app.utils.sentiment import analyze_sentiment
from flask_jwt_extended import jwt_required

sentiment_bp = Blueprint('sentiment', __name__)

@sentiment_bp.route('/analyze', methods=['POST'])
@jwt_required()
def analyze():
    data = request.get_json()
    text = data.get('text', '')

    if not text:
        return jsonify({"error": "Text is required"}), 400

    # Analyze sentiment
    scores = analyze_sentiment(text)

    # Optional: Customize the response format if needed
    return jsonify({
        "success": True,
        "sentiment_scores": scores
    }), 200
