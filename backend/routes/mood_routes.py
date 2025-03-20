from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import mysql.connector
from datetime import datetime
from db import get_db_connection # if get_db_connection is in app.py

mood_routes = Blueprint('mood_routes', __name__)
analyzer = SentimentIntensityAnalyzer()

@mood_routes.route('/track-mood', methods=['POST'])
@jwt_required()
def track_mood():
    data = request.get_json()
    user_id = get_jwt_identity()
    text = data.get("text")
    mood_score = data.get("mood_score")

    if not text or mood_score is None:
        return jsonify({"error": "Text and mood_score are required"}), 400

    sentiment_scores = analyzer.polarity_scores(text)
    sentiment = "positive" if sentiment_scores['compound'] > 0.05 else "negative" if sentiment_scores['compound'] < -0.05 else "neutral"

    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO mood_entries (user_id, text, mood_score, sentiment) VALUES (%s, %s, %s, %s)",
            (user_id, text, mood_score, sentiment)
        )
        conn.commit()
        cursor.close()
        conn.close()

        return jsonify({
            "message": "Mood tracked successfully",
            "sentiment": sentiment,
            "scores": sentiment_scores
        }), 201
    except Exception as e:
        print("DB Error:", e)
        return jsonify({"error": "Database error"}), 500
