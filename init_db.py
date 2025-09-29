import sqlite3
import pandas as pd

# --- Step 1: Connect to SQLite ---
conn = sqlite3.connect("movies.db")
cur = conn.cursor()

# --- Step 2: Drop tables if they exist (clean reset) ---
cur.execute("DROP TABLE IF EXISTS movies")
cur.execute("DROP TABLE IF EXISTS ratings")

# --- Step 3: Create tables ---
cur.execute("""
CREATE TABLE movies (
    movie_id INTEGER PRIMARY KEY,
    title TEXT NOT NULL,
    genres TEXT
)
""")

cur.execute("""
CREATE TABLE ratings (
    rating_id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    movie_id INTEGER NOT NULL,
    rating REAL NOT NULL,
    FOREIGN KEY (movie_id) REFERENCES movies(movie_id)
)
""")

# --- Step 4: Insert sample movies ---
movies = [
    (1, "The Shawshank Redemption", "Drama"),
    (2, "The Godfather", "Crime,Drama"),
    (3, "The Dark Knight", "Action,Crime,Drama"),
    (4, "Pulp Fiction", "Crime,Drama"),
    (5, "Forrest Gump", "Drama,Romance"),
    (6, "Inception", "Action,Adventure,Sci-Fi"),
    (7, "The Matrix", "Action,Sci-Fi"),
    (8, "Interstellar", "Adventure,Drama,Sci-Fi"),
    (9, "Fight Club", "Drama"),
    (10, "The Lord of the Rings: The Fellowship of the Ring", "Adventure,Fantasy")
]
cur.executemany("INSERT INTO movies (movie_id, title, genres) VALUES (?, ?, ?)", movies)

# --- Step 5: Insert sample ratings ---
ratings = [
    (1, 1, 5.0), (1, 2, 4.5), (1, 3, 5.0),   # User 1
    (2, 2, 5.0), (2, 4, 4.0), (2, 5, 4.5),   # User 2
    (3, 1, 4.0), (3, 6, 5.0), (3, 7, 4.5),   # User 3
    (4, 3, 5.0), (4, 8, 5.0), (4, 9, 4.5),   # User 4
    (5, 5, 4.0), (5, 10, 5.0), (5, 6, 4.5)   # User 5
]
cur.executemany("INSERT INTO ratings (user_id, movie_id, rating) VALUES (?, ?, ?)", ratings)

# --- Step 6: Commit and close ---
conn.commit()
conn.close()

print("✅ Database created and seeded with sample data!")
