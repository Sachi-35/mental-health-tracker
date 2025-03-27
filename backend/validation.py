def validate_mood_data(data):
    if not data:
        return {"error": "Request body is missing"}, 400

    mood_score = data.get("mood_score")
    text = data.get("text", "").strip()

    if mood_score is None or not isinstance(mood_score, (int, float)):
        return {"error": "Mood score must be a number"}, 400

    if not (0 <= mood_score <= 10):
        return {"error": "Mood score must be between 0 and 10"}, 400

    if not text:
        return {"error": "Text cannot be empty"}, 400

    return None  