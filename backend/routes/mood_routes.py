from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_cors import cross_origin
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from app import limiter
from db import get_db_connection
from datetime import datetime, timedelta

mood_routes = Blueprint('mood_routes', __name__)
analyzer = SentimentIntensityAnalyzer()

# Mood Tracking API (JWT Protected)
@limiter.limit("5 per minute")
@mood_routes.route('/track-mood', methods=['POST'])
@jwt_required()
def track_mood():
    try:
        data = request.get_json()
        user_id = get_jwt_identity()
        text = data.get("text")
        mood_score = data.get("mood_score")

        if not text or mood_score is None:
            return jsonify({"error": "Text and mood_score are required"}), 400

        sentiment_scores = analyzer.polarity_scores(text)
        sentiment = (
            "positive" if sentiment_scores['compound'] > 0.05
            else "negative" if sentiment_scores['compound'] < -0.05
            else "neutral"
        )

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO mood_entries (user_id, text, mood_score, sentiment, timestamp) VALUES (%s, %s, %s, %s, NOW())",
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
        return jsonify({"error": "Database error"}), 500


# Mood History API (JWT Protected)
@mood_routes.route('/mood-history', methods=['GET'])
@cross_origin()
@jwt_required()
def get_mood_history():
    user_id = get_jwt_identity()
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute(
            "SELECT id, text, mood_score, sentiment, timestamp FROM mood_entries WHERE user_id = %s ORDER BY timestamp DESC",
            (user_id,)
        )
        mood_entries = cursor.fetchall()
        cursor.close()
        conn.close()
        return jsonify({"mood_history": mood_entries}), 200
    except Exception as e:
        return jsonify({"error": "Failed to fetch mood history"}), 500


# Edit Mood Entry API
@mood_routes.route('/edit/<int:entry_id>', methods=['PUT'])
@cross_origin()
@jwt_required()
def edit_mood(entry_id):
    user_id = get_jwt_identity()
    data = request.get_json()
    mood_score = data.get("mood_score")
    note = data.get("note", "")

    if mood_score is None:
        return jsonify({"error": "Mood score is required"}), 400

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM mood_entries WHERE id = %s AND user_id = %s", (entry_id, user_id))
    existing = cursor.fetchone()
    if not existing:
        return jsonify({"error": "Mood entry not found or unauthorized"}), 404

    cursor.execute("""
        UPDATE mood_entries 
        SET mood_score = %s, note = %s, timestamp = %s 
        WHERE id = %s
    """, (mood_score, note, datetime.utcnow(), entry_id))

    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({"message": "Mood entry updated successfully"}), 200


# Delete Mood Entry API
@mood_routes.route('/delete/<int:entry_id>', methods=['DELETE'])
@jwt_required()
def delete_mood(entry_id):
    user_id = get_jwt_identity()
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM mood_entries WHERE id = %s AND user_id = %s", (entry_id, user_id))
    result = cursor.fetchone()
    if not result:
        return jsonify({"error": "Mood entry not found or unauthorized"}), 404

    cursor.execute("DELETE FROM mood_entries WHERE id = %s", (entry_id,))
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({"message": "Mood entry deleted successfully"}), 200


# Fetch User Mood Stats API
@mood_routes.route('/user/stats', methods=['GET'])
@jwt_required()
def user_mood_stats():
    user_id = get_jwt_identity()
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT COUNT(*) AS total_entries FROM mood_entries WHERE user_id = %s", (user_id,))
        total_entries = cursor.fetchone()['total_entries']

        if total_entries == 0:
            return jsonify({"message": "No mood entries found for user."}), 200

        cursor.execute("""
            SELECT mood_score, COUNT(*) AS count 
            FROM mood_entries WHERE user_id = %s 
            GROUP BY mood_score ORDER BY count DESC LIMIT 1
        """, (user_id,))
        most_common_mood = cursor.fetchone()

        last_week = (datetime.utcnow() - timedelta(days=7)).strftime('%Y-%m-%d')
        last_month = (datetime.utcnow() - timedelta(days=30)).strftime('%Y-%m-%d')

        cursor.execute("SELECT AVG(mood_score) AS avg_week_score FROM mood_entries WHERE user_id = %s AND timestamp >= %s", (user_id, last_week))
        avg_week_score = cursor.fetchone()['avg_week_score']

        cursor.execute("SELECT AVG(mood_score) AS avg_month_score FROM mood_entries WHERE user_id = %s AND timestamp >= %s", (user_id, last_month))
        avg_month_score = cursor.fetchone()['avg_month_score']

        cursor.execute("""
            SELECT SUM(CASE WHEN mood_score > 5 THEN 1 ELSE 0 END) AS positive_moods,
                   SUM(CASE WHEN mood_score < 5 THEN 1 ELSE 0 END) AS negative_moods
            FROM mood_entries WHERE user_id = %s
        """, (user_id,))
        mood_counts = cursor.fetchone()
        positive_percentage = (mood_counts['positive_moods'] / total_entries) * 100 if total_entries > 0 else 0
        negative_percentage = (mood_counts['negative_moods'] / total_entries) * 100 if total_entries > 0 else 0

        cursor.close()
        conn.close()
        return jsonify({
            "total_entries": total_entries,
            "most_common_mood": most_common_mood['mood_score'] if most_common_mood else None,
            "average_mood_score_last_week": avg_week_score,
            "average_mood_score_last_month": avg_month_score,
            "positive_mood_percentage": positive_percentage,
            "negative_mood_percentage": negative_percentage
        }), 200
    except Exception as e:
        return jsonify({"error": "Failed to fetch mood statistics"}), 500
