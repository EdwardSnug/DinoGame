# scores_db.py
import sqlite3

DB_FILE = "scores.db"

def init_db():
    """Initialize the database and create scores table if not exists."""
    conn = sqlite3.connect(DB_FILE)
    cur = conn.cursor()
    cur.execute('''
        CREATE TABLE IF NOT EXISTS scores (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            player_name TEXT NOT NULL,
            score INTEGER NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

def save_score(player_name, score):
    """Save a player's score into the database."""
    conn = sqlite3.connect(DB_FILE)
    cur = conn.cursor()
    cur.execute("INSERT INTO scores (player_name, score) VALUES (?, ?)", (player_name, score))
    conn.commit()
    conn.close()

def get_high_scores(limit=5):
    """Fetch top scores sorted in descending order."""
    conn = sqlite3.connect(DB_FILE)
    cur = conn.cursor()
    cur.execute("SELECT player_name, score FROM scores ORDER BY score DESC LIMIT ?", (limit,))
    results = cur.fetchall()
    conn.close()
    return results
