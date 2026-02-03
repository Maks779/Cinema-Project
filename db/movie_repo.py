from db.connection import get_db_connection

class MovieRepo:
    def get_all_movies(self):
        conn = get_db_connection()
        cursor = conn.cursor()
        # ENSURE 'poster_link' IS THE 6TH COLUMN
        cursor.execute("SELECT id, title, genre, duration, description, poster_link FROM movies")
        movies = cursor.fetchall()
        cursor.close()
        conn.close()
        return movies