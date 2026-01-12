import sys
import os

# Add project root to sys.path to import config/db
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from db.connection import get_db_connection


def create_tables():
    conn = get_db_connection()
    if conn is None:
        print("Failed to connect to the database.")
        return

    commands = [
        # 1. Users Table
        """
        CREATE TABLE IF NOT EXISTS users (
            id SERIAL PRIMARY KEY,
            username VARCHAR(50) UNIQUE NOT NULL,
            password_hash VARCHAR(255) NOT NULL,
            first_name VARCHAR(50),
            last_name VARCHAR(50),
            role VARCHAR(20) DEFAULT 'user',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """,
        # 2. Movies Table
        """
        CREATE TABLE IF NOT EXISTS movies (
            id SERIAL PRIMARY KEY,
            title VARCHAR(100) NOT NULL,
            description TEXT,
            duration_minutes INTEGER,
            genre VARCHAR(50),
            release_date DATE
        )
        """,
        # 3. Halls Table
        """
        CREATE TABLE IF NOT EXISTS halls (
            id SERIAL PRIMARY KEY,
            name VARCHAR(50) NOT NULL,
            total_seats INTEGER NOT NULL
        )
        """,
        # 4. Showtimes Table
        """
        CREATE TABLE IF NOT EXISTS showtimes (
            id SERIAL PRIMARY KEY,
            movie_id INTEGER REFERENCES movies(id) ON DELETE CASCADE,
            hall_id INTEGER REFERENCES halls(id) ON DELETE CASCADE,
            start_time TIMESTAMP NOT NULL,
            price DECIMAL(10, 2) NOT NULL
        )
        """,
        # 5. Bookings Table
        """
        CREATE TABLE IF NOT EXISTS bookings (
            id SERIAL PRIMARY KEY,
            user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
            showtime_id INTEGER REFERENCES showtimes(id) ON DELETE CASCADE,
            booking_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            total_price DECIMAL(10, 2)
        )
        """,
        # 6. Booked Seats (Many-to-Many for specific seats)
        """
        CREATE TABLE IF NOT EXISTS booked_seats (
            booking_id INTEGER REFERENCES bookings(id) ON DELETE CASCADE,
            seat_number VARCHAR(10) NOT NULL,
            PRIMARY KEY (booking_id, seat_number)
        )
        """
    ]

    try:
        cur = conn.cursor()
        for command in commands:
            cur.execute(command)

        # Create a default admin user if it doesn't exist (Password: admin)
        # Note: In production, use a proper hash! This is a placeholder hash.
        cur.execute("SELECT id FROM users WHERE username = 'admin'")
        if not cur.fetchone():
            cur.execute(
                "INSERT INTO users (username, password_hash, role) VALUES (%s, %s, %s)",
                ('admin', 'admin', 'admin')
            )
            print("Default admin account created (admin/admin).")

        conn.commit()
        cur.close()
        conn.close()
        print("Tables created successfully!")
    except Exception as e:
        print(f"Error creating tables: {e}")


if __name__ == "__main__":
    create_tables()