import mysql.connector
from flask import current_app

from db import get_db_connection

def execute_query(query, params=None, fetchone=False):
    try:
        with get_db_connection() as conn:
            with conn.cursor(dictionary=True) as cursor:
                cursor.execute(query, params or ())
                conn.commit()
                return cursor.fetchone() if fetchone else cursor.fetchall()
    except Exception as e:
        print(f"Database error: {e}")  # Use proper logging in production
        return None

def get_db_connection():
    return mysql.connector.connect(
        host=current_app.config['MYSQL_HOST'],
        user=current_app.config['MYSQL_USER'],
        password=current_app.config['MYSQL_PASSWORD'],
        database=current_app.config['MYSQL_DATABASE']
    )
