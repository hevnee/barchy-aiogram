import sqlite3
import os

db_file = "data/data.db"
os.makedirs(os.path.dirname(db_file), exist_ok=True)
database = sqlite3.connect(db_file)
cursor = database.cursor()

def create_tables():
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER UNIQUE NOT NULL,
            username TEXT,
            lang TEXT,
            register_date TEXT,
            history_position INTEGER DEFAULT 0,
            UNIQUE (user_id)
        )""")
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS request_history (
            user_id INTEGER NOT NULL,
            username TEXT,
            request_original TEXT,
            request_translation TEXT,
            response_original TEXT,
            response_translation TEXT,
            date TEXT,
            timestamp INTEGER
        )""")
    database.commit()
create_tables()


#CRUD operations
async def user_save(user, timestamp):
    cursor.execute("INSERT OR IGNORE INTO users (user_id, username, register_date) VALUES (?, ?, ?)", (user.id, user.username, timestamp))
    cursor.execute("UPDATE users SET username = ? WHERE user_id = ?", (user.username, user.id))
    database.commit()

def get_lang(user):
    cursor.execute("SELECT lang FROM users WHERE user_id = ?", (user.id,))
    lang = cursor.fetchone()
    return lang[0]

def get_currpage_resp(user):
    current_page = cursor.execute("SELECT history_position FROM users WHERE user_id = ?", (user.id,)).fetchone()[0]
    response = cursor.execute("SELECT request_original, response_translation, date, timestamp FROM request_history WHERE user_id = ? ORDER BY rowid", (user.id,)).fetchall()
    return current_page, response

def get_currpage_resp_original(user):
    current_page = cursor.execute("SELECT history_position FROM users WHERE user_id = ?", (user.id,)).fetchone()[0]
    response = cursor.execute("SELECT request_translation, response_original, date, timestamp FROM request_history WHERE user_id = ? ORDER BY rowid", (user.id,)).fetchall()
    return current_page, response

def update_history_position(current_page, user):
    cursor.execute("UPDATE users SET history_position = ? WHERE user_id = ?", (current_page, user.id))
    database.commit()