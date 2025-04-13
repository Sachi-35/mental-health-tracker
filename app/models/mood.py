from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from app.extensions import db

class Mood(db.Model):
    __tablename__ = 'mood_entries'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    mood = Column(String(50), nullable=False)
    note = Column(Text, nullable=True)
    timestamp = Column(DateTime, default=datetime.utcnow)
    quiz_data = db.Column(db.JSON, nullable=True)  # Store quiz answers in JSON format
    created_at = db.Column(db.DateTime, default=datetime.utcnow)  # Add created_at
    updated_at = db.Column(db.DateTime, onupdate=datetime.utcnow)  # Add updated_at

    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "mood": self.mood,
            "note": self.note,
            "timestamp": self.timestamp.isoformat(),
            "quiz_data": self.quiz_data,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None
        }