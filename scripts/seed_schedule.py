import random
import sys
import os
from datetime import datetime, timedelta
from dotenv import load_dotenv

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)
load_dotenv(os.path.join(BASE_DIR, ".env"))
from db.connection import get_db_connection


def seed_guaranteed_schedule():
    conn = get_db_connection()
    cur = conn.cursor()

    print("🧹 Clearing old showtimes...")
    cur.execute("TRUNCATE TABLE showtimes RESTART IDENTITY CASCADE;")

    cur.execute("SELECT id, duration FROM movies;")
    all_movies = cur.fetchall()

    start_date = datetime.now().date()
    # Seed for 12 months
    for month in range(12):
        month_start = start_date + timedelta(days=month * 30)
        print(f"📅 Seeding Month {month + 1}...")

        # Shuffle movies so they appear on different days each month
        random.shuffle(all_movies)

        for i, (movie_id, duration) in enumerate(all_movies):
            # Distribute movies across the 30 days of the month
            day_offset = i % 30
            show_date = month_start + timedelta(days=day_offset)
            room_id = (i % 10) + 1

            # Set a random start time between 10 AM and 8 PM
            start_time = datetime.combine(show_date, datetime.min.time()) + \
                         timedelta(hours=random.randint(10, 20))
            end_time = start_time + timedelta(minutes=duration)
            price = round(random.uniform(12.0, 22.0), 2)

            cur.execute("""
                INSERT INTO showtimes (movie_id, room_id, start_time, end_time, price)
                VALUES (%s, %s, %s, %s, %s)
            """, (movie_id, room_id, start_time, end_time, price))

    conn.commit()
    cur.close()
    conn.close()
    print("✅ Success! Every movie now has at least one show per month for the next year.")


if __name__ == "__main__":
    seed_guaranteed_schedule()