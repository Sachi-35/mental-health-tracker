import os
import urllib.parse
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "secure_password_2025")
    MYSQL_HOST = os.getenv("MYSQL_HOST", "localhost")
    MYSQL_USER = os.getenv("MYSQL_USER", "root")
    MYSQL_PASSWORD = urllib.parse.quote_plus(os.getenv("MYSQL_PASSWORD", "Sachi@2005"))
    MYSQL_DB = os.getenv("MYSQL_DB", "mental_health_tracker")

    SQLALCHEMY_DATABASE_URI = (
        f"mysql://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}/{MYSQL_DB}"
    )
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "secure_password_2025")
