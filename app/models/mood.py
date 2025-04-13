from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from app.extensions import db

class Mood(db.Model):
    __tablename__ = 'mood_entries'  # Ensure this matches the actual table name in the DB

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)  # Foreign key to users table
    mood = Column(String(50), nullable=False)  # Mood column (e.g., happy, sad, etc.)
    note = Column(Text, nullable=True)  # Optional note for additional info
    timestamp = Column(DateTime, default=datetime.utcnow)  # Timestamp when the mood is logged
    quiz_data = db.Column(db.JSON, nullable=True)  # This will store the quiz answers in JSON format

    def to_dict(self):
        """
        Converts the Mood instance to a dictionary format
        to be used for JSON responses.
        """
        return {
            "id": self.id,
            "user_id": self.user_id,
            "mood": self.mood,
            "note": self.note,
            "timestamp": self.timestamp.isoformat(),  # Convert datetime to ISO format
            "quiz_data": self.quiz_data  # This will include the quiz data if it's set
        }