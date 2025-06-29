import sqlite3, os
from config import BotConfigs
from datetime import datetime
from typing import Optional

os.makedirs(os.path.dirname(BotConfigs.DATABASE_FILE), exist_ok=True)

database = sqlite3.connect(BotConfigs.DATABASE_FILE)
cursor = database.cursor()

def create_tables():
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER UNIQUE,
            username TEXT,
            full_name TEXT,
            lang TEXT,
            history_position INTEGER DEFAULT 0,
            AI_style TEXT DEFAULT normal,
            register_date TEXT,
            last_interaction TEXT
        )""")
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS request_history (
            user_id INTEGER NOT NULL,
            request_original TEXT,
            request_translation TEXT,
            response_original TEXT,
            response_translation TEXT,
            date TEXT,
            timestamp INTEGER
        )""")
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS dick_game (
            user_id INTEGER UNIQUE,
            active_chats TEXT,
            size INTEGER DEFAULT 0,
            last_used INTEGER DEFAULT 0
        )""")
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS giveaways (
            creator_id INTEGER,
            chat_id INTEGER UNIQUE,
            message_id INTEGER,
            users TEXT,
            size INTEGER,
            timestamp_start INTEGER,
            timestamp_end INTEGER,
            status TEXT,
            winner INTEGER
        )""")
    database.commit()
create_tables()

def user_save(user) -> None:
    date_time = datetime.now().strftime("%d.%m.%Y %H:%M:%S")
    cursor.execute("INSERT OR IGNORE INTO users (user_id, username, full_name, register_date, last_interaction) VALUES (?, ?, ?, ?, ?)", (user.id, user.username, user.full_name, date_time, date_time))
    cursor.execute("UPDATE users SET last_interaction = ?, username = ? WHERE user_id = ?", (date_time, user.username, user.id))
    cursor.execute("INSERT OR IGNORE INTO dick_game (user_id) VALUES (?)", (user.id,))
    database.commit()

def get_lang(user_id: int) -> Optional[str]:
    return cursor.execute("SELECT lang FROM users WHERE user_id = ?", (user_id,)).fetchone()[0]