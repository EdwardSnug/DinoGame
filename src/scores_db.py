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

def delete_score_by_name(player_name):
    """Delete all scores for a player from the database by name."""
    conn = sqlite3.connect(DB_FILE)
    cur = conn.cursor()
    cur.execute("DELETE FROM scores WHERE player_name = ?", (player_name,))
    conn.commit()
    conn.close()
    print(f"All scores for '{player_name}' have been deleted.")

def update_player_name(old_name, new_name):
    """Updates a player's name in the database."""
    conn = sqlite3.connect(DB_FILE)
    cur = conn.cursor()
    cur.execute("UPDATE scores SET player_name = ? WHERE player_name = ?", (new_name, old_name))
    conn.commit()
    conn.close()
    print(f"Player name updated from '{old_name}' to '{new_name}'.")

def delete_all_scores():
    """Delete all scores from the database."""
    conn = sqlite3.connect(DB_FILE)
    cur = conn.cursor()
    cur.execute("DELETE FROM scores")
    conn.commit()
    conn.close()
    print("All scores have been deleted.")