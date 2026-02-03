import csv
from db.connection import get_db_connection


def import_imdb_movies(csv_file_path):
    conn = get_db_connection()
    cursor = conn.cursor()

    print("🚀 Cleaning old data and starting fresh import...")

    # Clear old data so we don't have duplicates or "None min" entries
    cursor.execute("TRUNCATE TABLE movies RESTART IDENTITY CASCADE;")

    with open(csv_file_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)

        count = 0
        for row in reader:
            if count >= 50:
                break

            # Match CSV headers exactly from imdb_top_1000.csv
            title = row['Series_Title']
            genre = row['Genre']
            description = row['Overview']
            poster_url = row['Poster_Link']  # Fixes "No Image"

            # Fixes "None min": Extract numbers from "142 min"
            try:
                runtime_str = row['Runtime']
                duration = int(''.join(filter(str.isdigit, runtime_str)))
            except:
                duration = 120  # Fallback

            # Insert into database with ALL 5 columns (ID is auto-generated)
            cursor.execute("""
                INSERT INTO movies (title, genre, duration, description, poster_link)
                VALUES (%s, %s, %s, %s, %s)
            """, (title, genre, duration, description, poster_url))

            count += 1

    conn.commit()
    cursor.close()
    conn.close()
    print(f"✅ Successfully imported {count} movies with Posters and Runtimes!")


if __name__ == "__main__":
    import_imdb_movies("imdb_top_1000.csv")