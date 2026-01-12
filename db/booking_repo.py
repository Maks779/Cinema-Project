from db.connection import get_db_connection


class BookingRepo:
    def create_booking(self, user_id, showtime_id, seat_numbers):
        conn = get_db_connection()
        if not conn: return False
        try:
            cur = conn.cursor()
            # 1. Insert into bookings table
            cur.execute(
                "INSERT INTO bookings (user_id, showtime_id) VALUES (%s, %s) RETURNING id",
                (user_id, showtime_id)
            )
            booking_id = cur.fetchone()[0]

            # 2. Insert each seat into booked_seats
            for seat in seat_numbers:
                cur.execute(
                    "INSERT INTO booked_seats (booking_id, seat_number) VALUES (%s, %s)",
                    (booking_id, seat)
                )

            conn.commit()
            return True
        except Exception as e:
            print(f"Booking error: {e}")
            conn.rollback()
            return False
        finally:
            conn.close()