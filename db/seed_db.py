from db.connection import get_db_connection


def seed_data():
    conn = get_db_connection()
    if not conn:
        print("Failed to connect.")
        return

    try:
        cur = conn.cursor()

        # 1. Create a Hall
        print("Creating Hall...")
        cur.execute("INSERT INTO halls (name, total_seats) VALUES ('Hall A', 50) ON CONFLICT DO NOTHING;")

        # 2. Add Movies
        print("Adding Movies...")
        movies = [
            ("The Matrix", "Sci-Fi", 136, "A hacker discovers reality is a simulation."),
            ("Avatar: Way of Water", "Sci-Fi", 192, "Jake Sully lives with his newfound family.")
        ]

        for title, genre, duration, desc in movies:
            cur.execute("""
                INSERT INTO movies (title, genre, duration_minutes, description) 
                VALUES (%s, %s, %s, %s)
                ON CONFLICT DO NOTHING;
            """, (title, genre, duration, desc))

        # 3. Add Showtimes (linking Movies to Hall A)
        print("Scheduling Showtimes...")
        # Get IDs
        cur.execute("SELECT id FROM halls WHERE name = 'Hall A'")
        hall_id = cur.fetchone()[0]

        cur.execute("SELECT id, title FROM movies")
        movie_rows = cur.fetchall()  # [(1, 'The Matrix'), (2, 'Avatar')]

        # Add a showtime for each movie
        # Format: YYYY-MM-DD HH:MM:SS
        times = ["2026-01-14 18:00:00", "2026-01-14 21:00:00"]

        for i, (movie_id, title) in enumerate(movie_rows):
            if i < len(times):
                cur.execute("""
                    INSERT INTO showtimes (movie_id, hall_id, start_time, price)
                    VALUES (%s, %s, %s, 15.00)
                """, (movie_id, hall_id, times[i]))

        conn.commit()
        print("Database populated successfully!")

    except Exception as e:
        print(f"Error seeding data: {e}")
        conn.rollback()
    finally:
        conn.close()


if __name__ == "__main__":
    seed_data()