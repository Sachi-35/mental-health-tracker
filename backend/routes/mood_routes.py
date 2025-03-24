from flask import Blueprint, request, jsonify
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from flask_jwt_extended import jwt_required, get_jwt_identity
from db import get_db_connection

mood_routes = Blueprint('mood_routes', __name__)
analyzer = SentimentIntensityAnalyzer()

# Mood Tracking API (JWT Protected)
@mood_routes.route('/track-mood', methods=['POST'])
@jwt_required()
def track_mood():
    print("/track-mood hit")

    try:
        data = request.get_json()
        print("Received JSON:", data)
    except Exception as e:
        print("JSON error:", e)
        return jsonify({"error": "Invalid JSON"}), 400

    user_id = get_jwt_identity()
    print("Authenticated user ID:", user_id)

    if not data:
        return jsonify({"error": "Missing request body"}), 400

    text = data.get("text")
    mood_score = data.get("mood_score")

    if not text or mood_score is None:
        return jsonify({"error": "Text and mood_score are required"}), 400

    try:
        sentiment_scores = analyzer.polarity_scores(text)
        sentiment = (
            "positive" if sentiment_scores['compound'] > 0.05
            else "negative" if sentiment_scores['compound'] < -0.05
            else "neutral"
        )

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO mood_entries (user_id, text, mood_score, sentiment) VALUES (%s, %s, %s, %s)",
            (user_id, text, mood_score, sentiment)
        )
        conn.commit()
        cursor.close()
        conn.close()

        print("Mood saved to DB")
        return jsonify({
            "message": "Mood tracked successfully",
            "sentiment": sentiment,
            "scores": sentiment_scores
        }), 201

    except Exception as e:
        print("DB error:", e)
        return jsonify({"error": "Database error"}), 500

# Mood History API (JWT Protected)
@mood_routes.route('/mood-history', methods=['GET'])
@jwt_required()
def get_mood_history():
    print("Mood history requested")
    user_id = get_jwt_identity()
    print("Authenticated user ID:", user_id)

    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute(
            """
            SELECT id, text, mood_score, sentiment, created_at
            FROM mood_entries
            WHERE user_id = %s
            ORDER BY created_at DESC
            """,
            (user_id,)
        )

        mood_entries = cursor.fetchall()
        cursor.close()
        conn.close()

        return jsonify({"mood_history": mood_entries}), 200

    except Exception as e:
        print("Error fetching mood history:", e)
        return jsonify({"error": "Failed to fetch mood history"}), 500

# 🔐 Test JWT Route
@mood_routes.route('/test-protected', methods=['GET'])
@jwt_required()
def protected():
    current_user = get_jwt_identity()
    print("Authenticated user:", current_user)
    return jsonify(logged_in_as=current_user), 200
