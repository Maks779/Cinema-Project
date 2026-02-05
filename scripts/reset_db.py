import sys
import os
from dotenv import load_dotenv

# Path setup to find db and .env
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)
load_dotenv(os.path.join(BASE_DIR, ".env"))

from db.connection import get_db_connection


def fix_database_schema():
    conn = get_db_connection()
    cur = conn.cursor()
    try:
        print("🛠️  Updating database schema...")

        # 1. Create the showtimes table if it doesn't exist
        cur.execute("""
            CREATE TABLE IF NOT EXISTS showtimes (
                id SERIAL PRIMARY KEY,
                movie_id INTEGER REFERENCES movies(id) ON DELETE CASCADE,
                room_id INTEGER, 
                start_time TIMESTAMP,
                end_time TIMESTAMP
            );
        """)

        # 2. Add missing columns one by one just in case
        cur.execute("ALTER TABLE showtimes ADD COLUMN IF NOT EXISTS room_id INTEGER;")
        cur.execute("ALTER TABLE showtimes ADD COLUMN IF NOT EXISTS end_time TIMESTAMP;")

        # 3. Clean up existing data for a fresh start
        cur.execute("TRUNCATE TABLE movies, showtimes RESTART IDENTITY CASCADE;")

        conn.commit()
        print("✅ Schema fixed! room_id and end_time are now ready.")

    except Exception as e:
        print(f"❌ Error during schema update: {e}")
        conn.rollback()
    finally:
        cur.close()
        conn.close()


if __name__ == "__main__":
    fix_database_schema()