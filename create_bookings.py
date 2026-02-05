from db.connection import get_db_connection
from datetime import date


def force_test_booking():
    conn = get_db_connection()
    cur = conn.cursor()

    # 1. Targeted search for the exact screening in your screenshot
    # Change 'The Godfather' to 'The Shawshank Redemption' if needed
    target_movie = "The Godfather"
    target_date = date(2026, 2, 20)

    cur.execute("""
        SELECT s.id FROM showtimes s
        JOIN movies m ON s.movie_id = m.id
        WHERE m.title = %s AND s.start_time::date = %s
        LIMIT 1
    """, (target_movie, target_date))

    result = cur.fetchone()
    if not result:
        print(f"❌ Could not find a showtime for {target_movie} on {target_date}")
        return

    sid = result[0]

    # 2. Get a valid user
    cur.execute("SELECT id FROM users LIMIT 1")
    uid = cur.fetchone()[0]

    # 3. Insert specific seats
    test_seats = ['A1', 'A2', 'A3', 'C5', 'H10']
    print(f"🛠️ Booking seats for {target_movie} (ID: {sid})...")

    for seat in test_seats:
        cur.execute("""
            INSERT INTO bookings (user_id, showtime_id, seat_id) 
            VALUES (%s, %s, %s) 
            ON CONFLICT DO NOTHING
        """, (uid, sid, seat))

    conn.commit()
    print(f"✅ Success! Seats {test_seats} are now BOOKED in the database.")
    cur.close();
    conn.close()


if __name__ == "__main__":
    force_test_booking()