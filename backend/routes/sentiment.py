from flask import Blueprint, request, jsonify
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

sentiment_bp = Blueprint('sentiment', __name__)
analyzer = SentimentIntensityAnalyzer()

@sentiment_bp.route('/analyze', methods=['POST'])
def analyze_sentiment():
    data = request.get_json()
    text = data.get('text')

    if not text:
        return jsonify({"error": "No text provided"}), 400

    scores = analyzer.polarity_scores(text)

    # Example: classify overall sentiment
    sentiment = 'positive' if scores['compound'] >= 0.05 else 'negative' if scores['compound'] <= -0.05 else 'neutral'

    return jsonify({
        "text": text,
        "sentiment": sentiment,
        "scores": scores
    }), 200
