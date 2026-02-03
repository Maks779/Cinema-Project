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


def verify_database_schema():
    """Ensures the database has all required columns before the app starts."""
    conn = get_db_connection()
    if not conn:
        return

    try:
        cursor = conn.cursor()
        # This adds the duration column only if it doesn't already exist
        print("🔍 Checking database schema...")
        cursor.execute("ALTER TABLE movies ADD COLUMN IF NOT EXISTS duration INTEGER;")
        conn.commit()
        print("✅ Schema is up to date.")
    except Exception as e:
        print(f"⚠️ Schema update skipped or failed: {e}")
    finally:
        cursor.close()
        conn.close()