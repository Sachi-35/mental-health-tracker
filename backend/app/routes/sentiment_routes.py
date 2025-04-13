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
    
    # Get sentiment label based on compound score
    sentiment_label = "neutral"
    if scores['compound'] >= 0.05:
        sentiment_label = "positive"
    elif scores['compound'] <= -0.05:
        sentiment_label = "negative"

    # Return sentiment label and scores
    return jsonify({
        "success": True,
        "sentiment_label": sentiment_label,
        "sentiment_scores": scores
    }), 200
