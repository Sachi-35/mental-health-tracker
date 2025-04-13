from datetime import datetime
from app.extensions import db

class QuizResponse(db.Model):
    __tablename__ = 'quiz_responses'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    quiz_id = db.Column(db.Integer, nullable=False)  # Change 'question' to 'quiz_id'
    response = db.Column(db.String(255), nullable=False)  # Change 'answer' to 'response'
    created_at = db.Column(db.DateTime, default=datetime.utcnow)  # Add created_at
    updated_at = db.Column(db.DateTime, onupdate=datetime.utcnow)  # Add updated_at

    def __repr__(self):
        return f"<QuizResponse {self.quiz_id} - {self.response} by User {self.user_id}>"
