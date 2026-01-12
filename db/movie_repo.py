from db.connection import get_db_connection

class MovieRepo:
    def get_all_movies(self):
        conn = get_db_connection()
        if not conn: return []
        try:
            cur = conn.cursor()
            cur.execute("SELECT id, title, genre, duration_minutes, description FROM movies")
            return cur.fetchall()
        except Exception as e:
            print(f"Error fetching movies: {e}")
            return []
        finally:
            conn.close()