from flask import Blueprint

# Import blueprints from other route files
from .auth_routes import auth_bp
from .mood_routes import mood_bp
from .sentiment_routes import sentiment_bp
from .quiz_routes import quiz_bp  # <-- new route

# Create a Blueprint to group them (optional, only if nesting)
routes_bp = Blueprint('routes', __name__)

# You can register the blueprints here if you're grouping, or do it in app/__init__.py
def register_routes(app):
    app.register_blueprint(auth_bp)
    app.register_blueprint(mood_bp)
    app.register_blueprint(sentiment_bp)
    app.register_blueprint(quiz_bp)  # <-- register the new quiz route
