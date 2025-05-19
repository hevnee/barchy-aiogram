from configs.languages_dict import *

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram import Bot, Dispatcher, types
from aiogram.enums import ParseMode
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from aiogram.filters import Command
from aiogram.types import Message
from datetime import datetime
from collections import deque
from aiogram import F
import time as times
import asyncio
import logging
import sqlite3
import requests
import os

TOKEN = "TOKEN"

MAX_HISTORY_LENGTH = 25
MEMORY_DURATION = 3600

db_file = "data/logs.db"
os.makedirs(os.path.dirname(db_file), exist_ok=True)

database_logs = sqlite3.connect(db_file)
cursor_logs = database_logs.cursor()

def create_tables():
    cursor_logs.execute("""
        CREATE TABLE IF NOT EXISTS users_logs (
            user_id INTEGER NOT NULL,
            username TEXT,
            time TEXT,
            lang TEXT,
            UNIQUE (user_id)
        )""")
    cursor_logs.execute("""
        CREATE TABLE IF NOT EXISTS requests (
            user_id INTEGER NOT NULL,
            username TEXT,
            request TEXT,
            answer_original TEXT,
            answer_translation TEXT,
            time TEXT,
            action_time INTEGER,
            UNIQUE (user_id, time)
        )""")
    database_logs.commit()
create_tables()

def user_save(user_id, username, time):
    cursor_logs.execute("INSERT OR IGNORE INTO users_logs (user_id, username, time) VALUES (?, ?, ?)", (user_id, username, time))
    cursor_logs.execute("UPDATE users_logs SET username = ? WHERE user_id = ?", (username, user_id))
    database_logs.commit()

def get_lang(user_id):
    cursor_logs.execute("SELECT lang FROM users_logs WHERE user_id = ?", (user_id,))
    lang = cursor_logs.fetchone()[0]
    return lang

def get_lang_example(user_id):
    cursor_logs.execute("SELECT lang FROM users_logs WHERE user_id = ?", (user_id,))
    lang = cursor_logs.fetchone()
    return lang

language_keyboard = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(text="🇷🇺 Русский", callback_data="ru"),
        InlineKeyboardButton(text="🇺🇦 Українська", callback_data="ua")
    ],
    [
        InlineKeyboardButton(text="🇬🇧 English", callback_data="en"),
        InlineKeyboardButton(text="🇵🇱 Polski", callback_data="pl")
    ],
    [
        InlineKeyboardButton(text="🇩🇪 Deutsch", callback_data="de"),
        InlineKeyboardButton(text="🇫🇷 Français", callback_data="fr")
    ],
    [
        InlineKeyboardButton(text="🇪🇸 Español", callback_data="es"),
        InlineKeyboardButton(text="🇹🇷 Türkiye", callback_data="tr")
    ]
])