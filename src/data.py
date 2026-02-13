import sqlite3
import os
#------------------------------
DB_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "Cinema03.db"))
#------------------------------
def get_conn():
    return sqlite3.connect(DB_PATH, check_same_thread=False)
#------------------------------
def init_db():
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("""
    CREATE TABLE IF NOT EXISTS movie(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        movie_name TEXT,
        release_year INTEGER,
        actor_numbers INTEGER,
        budjet REAL,
        genre TEXT NOT NULL,
        director TEXT
    )
    """)
    conn.commit()
    conn.close()
#------------------------------
def insert_movie(movie_name, release_year, actor_numbers, budjet, genre, director):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO movie(movie_name, release_year, actor_numbers, budjet, genre, director)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (movie_name, release_year, actor_numbers, budjet, genre, director))
    conn.commit()
    conn.close()
#------------------------------
def get_all_movies():
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("""
        SELECT id, movie_name, release_year, actor_numbers, budjet, genre, director
        FROM movie
        ORDER BY id DESC
    """)
    rows = cur.fetchall()
    conn.close()
    
    return rows
#------------------------------
def search_local_movies(query):
    q = f"%{query}%"
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("""
        SELECT id, movie_name, release_year, actor_numbers, budjet, genre, director
        FROM movie
        WHERE movie_name LIKE ? OR director LIKE ? OR genre LIKE ?
        ORDER BY id DESC
    """, (q, q, q))
    rows = cur.fetchall()
    conn.close()

    return rows
#------------------------------
def get_stats():
    conn = get_conn()
    cur = conn.cursor()

    cur.execute("SELECT COUNT(*) FROM movie")
    total = cur.fetchone()[0]

    cur.execute("SELECT COUNT(DISTINCT genre) FROM movie")
    genres = cur.fetchone()[0]

    cur.execute("SELECT AVG(release_year) FROM movie")
    avg_year = cur.fetchone()[0]

    conn.close()

    return total, genres, avg_year
#------------------------------
def get_latest_movies(limit=5):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("""
        SELECT id, movie_name, release_year, genre, director
        FROM movie
        ORDER BY id DESC
        LIMIT ?
    """, (limit,))
    rows = cur.fetchall()
    conn.close()

    return rows

