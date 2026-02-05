import csv
import sys
import os
from dotenv import load_dotenv

# 1. Find the path of the main project folder
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# 2. Add it to the system path so it can find the 'db' and 'config' folders
sys.path.append(BASE_DIR)

# 3. Explicitly load the .env file from the main folder
load_dotenv(os.path.join(BASE_DIR, ".env"))

# NOW you can do your imports
from db.connection import get_db_connection

def import_imdb_movies(csv_file_path):
    conn = get_db_connection()
    cursor = conn.cursor()

    print("🚀 Cleaning database and importing Top 250 movies...")
    # Truncate ensures we start fresh with ID #1
    cursor.execute("TRUNCATE TABLE movies RESTART IDENTITY CASCADE;")

    if not os.path.exists(csv_file_path):
        print(f"❌ Error: Could not find CSV at {csv_file_path}")
        return

    with open(csv_file_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        count = 0
        for row in reader:
            if count >= 250:
                break

            cursor.execute("""
                INSERT INTO movies (title, genre, duration, description, poster_link)
                VALUES (%s, %s, %s, %s, %s)
            """, (row['Series_Title'], row['Genre'],
                  int(''.join(filter(str.isdigit, row['Runtime']))),
                  row['Overview'], row['Poster_Link']))
            count += 1

    conn.commit()
    cursor.close()
    conn.close()
    print(f"✅ Successfully imported {count} movies into the database.")

if __name__ == "__main__":
    # Points to the new data folder location
    DATA_PATH = os.path.join(os.path.dirname(__file__), '..', 'data', 'imdb_top_1000.csv')
    import_imdb_movies(DATA_PATH)