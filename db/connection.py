import psycopg2
from config import settings

def get_db_connection():
    """Establishes a connection to the PostgreSQL database using config settings."""
    try:
        conn = psycopg2.connect(
            host=settings.db.host,
            port=settings.db.port,
            user=settings.db.user,
            password=settings.db.password,
            dbname=settings.db.dbname
        )
        return conn
    except Exception as e:
        print(f"Error connecting to database: {e}")
        return None