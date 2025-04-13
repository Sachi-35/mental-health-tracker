from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models.mood import Mood
from app.extensions import db
import datetime

mood_bp = Blueprint('mood', __name__)

@mood_bp.route('/add_mood', methods=['POST'])
@jwt_required()
def add_mood():
    # Debug: check request content type
    print("Content-Type:", request.content_type)
    if not request.is_json:
        print("Not JSON!")
        return jsonify({"success": False, "message": "Expected JSON"}), 400

    # Safely parse JSON
    data = request.get_json(silent=True)
    print("Raw JSON:", data)

    if not data or "mood" not in data:
        return jsonify({"success": False, "message": "Mood is required"}), 400

    mood = data["mood"]
    quiz_data = data.get("quiz_data", {})  # Optional quiz data (default to empty dictionary)
    user_id = get_jwt_identity()

    # Create mood entry with optional quiz_data
    new_mood = Mood(user_id=user_id, mood=mood, quiz_data=quiz_data)
    db.session.add(new_mood)
    db.session.commit()

    return jsonify({"success": True, "message": "Mood saved"}), 200


@mood_bp.route('/get_mood', methods=['GET'])
@jwt_required()
def get_mood():
    user_id = get_jwt_identity()
    moods = Mood.query.filter_by(user_id=user_id).order_by(Mood.timestamp.desc()).all()

    if not moods:
        return jsonify({"success": False, "message": "No mood data found"}), 404

    # Sentiment Analysis Logic
    sentiment = None
    suggestion = None
    mood_count = {"positive": 0, "neutral": 0, "negative": 0}

    for mood_entry in moods:
        mood = mood_entry.mood.lower()
        if mood in ["sad", "anxious", "stressed"]:
            mood_count["negative"] += 1
        elif mood in ["happy", "calm", "excited"]:
            mood_count["positive"] += 1
        else:
            mood_count["neutral"] += 1

    # Analyze mood counts for sentiment
    if mood_count["positive"] > mood_count["negative"]:
        sentiment = "Positive"
        suggestion = "Keep up the good work!"
    elif mood_count["negative"] > mood_count["positive"]:
        sentiment = "Negative"
        suggestion = "Consider taking some time for self-care."
    else:
        sentiment = "Neutral"
        suggestion = "Stay balanced, take it easy."

    # Data for mood chart (Example: Show mood count by day)
    mood_data = [{"date": mood.timestamp.strftime('%Y-%m-%d'), "mood": mood.mood} for mood in moods]

    # Create chart data (e.g., aggregate mood counts by day)
    mood_by_day = {}
    for entry in mood_data:
        date = entry["date"]
        if date not in mood_by_day:
            mood_by_day[date] = {"positive": 0, "neutral": 0, "negative": 0}
        mood = entry["mood"].lower()
        if mood in ["sad", "anxious", "stressed"]:
            mood_by_day[date]["negative"] += 1
        elif mood in ["happy", "calm", "excited"]:
            mood_by_day[date]["positive"] += 1
        else:
            mood_by_day[date]["neutral"] += 1

    chart_data = [{"date": date, "positive": counts["positive"], "neutral": counts["neutral"], "negative": counts["negative"]} for date, counts in mood_by_day.items()]

    return jsonify({
        "success": True,
        "moods": [m.to_dict() for m in moods],
        "sentiment": sentiment,
        "suggestion": suggestion,
        "chart_data": chart_data  # Return chart data to frontend
    }), 200
