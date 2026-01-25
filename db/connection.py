import psycopg2
from config import settings

def get_db_connection():
    """Establishes a connection to the PostgreSQL database using config settings."""
    try:
        conn = psycopg2.connect(
            host=settings.db.DB_HOST,
            port=settings.db.DB_PORT,
            user=settings.db.DB_USER,
            password=settings.db.DB_PASSWORD,
            dbname=settings.db.DB_NAME
        )
        return conn
    except Exception as e:
        print(f"Error connecting to database: {e}")
        return None