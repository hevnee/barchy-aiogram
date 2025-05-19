import os
from aiogram import Bot, Dispatcher, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.enums import ParseMode
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from aiogram.filters import Command
from aiogram.types import Message
from datetime import datetime
import logging
import sqlite3
import asyncio

TOKEN = "TOKEN"

os.makedirs(os.path.dirname("logs.db"), exist_ok=True)
database = sqlite3.connect("logs.db")
cursor = database.cursor()

def create_tables():
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users_logs (
            user_id INTEGER NOT NULL,
            username TEXT,
            time TEXT,
            lang TEXT,
            UNIQUE (user_id)
        )""")
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS requests (
            user_id INTEGER NOT NULL,
            username TEXT,
            request TEXT,
            answer_en TEXT,
            answer_ru TEXT,
            time TEXT,
            action_time INTEGER
        )""")
    database.commit()

def saving(user_id, username, time):
    cursor.execute("INSERT OR IGNORE INTO users_logs (user_id, username, time) VALUES (?, ?, ?)", (user_id, username, time))
    cursor.execute("UPDATE users_logs SET username = ? WHERE user_id = ?", (username, user_id))
    database.commit()

def get_lang(user_id):
    cursor.execute("SELECT lang FROM users_logs WHERE user_id = ?", (user_id,))
    lang = cursor.fetchone()[0]
    return lang

languages = (
    "ru", "ua", "en", "pl",
    "fr", "de", "kz", "cn",
)

select_language = {
    "ru": {
        "change_language": "Язык:",
        
        "change_language_succesfully": "Язык успешно изменён!",
        
        "welcome_text": (
            "🤖 Привет! Я бот по имени barchy.\n"
            "В моём арсенале есть несколько крутых функций!\n"
            "Чтобы их узнать пропиши комманду <code>/commands</code>\n\n"
        ),
        "tech_works": (
            "<b>⚙️ Технические работы ⚙️</b>\n"
            "<b>Внимание!</b> В данный момент часть бота с ИИ не работает\n"
        ),
        "welcome_tech_works": (
            "🤖 Привет! Я бот по имени barchy.\n"
            "В моём арсенале есть несколько крутых функций!\n"
            "Чтобы их узнать пропиши комманду <code>/commands</code>\n\n"
            "<b>⚙️ Технические работы ⚙️</b>\n"
            "<b>Внимание!</b> В данный момент часть бота с ИИ не работает\n"
        ),
        "commands": (
            "<b>Общение с ИИ</b>\n"
            "<code>/chat [Ваш запрос]</code> - общение с ИИ\n"
            "<code>/forget</code> - забыть весь диалог\n\n"
            "<b>Другие функции</b>\n"
            "<code>/language</code> - сменить язык\n"
        ),
        "translating_request": "Переводим ваш запрос...",
        
        "request_processed": "Ваш запрос обрабатывается...",
        
        "translating_text": "Переводим...",
        
        "forget_clear": "История разговора очищена!",
        
        "just_chat": "Пожалуйста, укажите текст после команды /chat",
        
        "show_original_lang": "Показать оригинал",
    },
    
    "ua": {
        "change_language": "Мова:",
        
        "change_language_succesfully": "Мова успішно змінена!",
        
        "welcome_text": (
            "🤖 Хай! Я бот з іменем barchy.\n"
            "В моєму арсеналі є декілька крутих функцій!\n"
            "Щоб дізнатися їх, введіть команду <code>/commands</code>\n\n"
        ),
        
        "tech_works": (
            "<b>⚙️ Технічні роботи ⚙️</b>\n"
            "<b>Увага!</b> У даний момент частинка бота з ШІ бота\n"
        ),
        
        "welcome_tech_works": (
            "🤖 Хай! Я бот з іменем barchy.\n"
            "В моєму арсеналі є декілька крутих функцій!\n"
            "Щоб дізнатися їх, введіть команду <code>/commands</code>\n\n"
            "<b>⚙️ Технічні роботи ⚙️</b>\n"
            "<b>Увага!</b> У даний момент частинка бота з ШІ бота\n"
        ),
        
        "commands": (
            "<b>Спілкування з ШІ</b>\n"
            "<code>/chat [Ваш запит]</code> - спілкування з ШІ\n"
            "<code>/forget</code> - забути весь діалог\n\n"
            "<b>Інші функції</b>\n"
            "<code>/language</code> - змінити мову\n"
        ),
        "translating_request": "Перекладаємо ваш запит...",
        
        "request_processed": "Ваш запит обробляється...",
        
        "translating_text": "Перекладаємо...",
        
        "forget_clear": "Історію розмови очищено!",
        
        "just_chat": "Будь ласка, вкажіть текст після команди /chat",
        
        "show_original_lang": "Показати оригінал",
    },
    
    "en": {
        "change_language": "Language:",
        
        "change_language_succesfully": "Language successfully changed!",
        
        "welcome_text": (
            "🤖 Hi! I'm a bot named barchy.\n"
            "I have some cool features in my arsenal!\n"
            "To find them out, type the command <code>/commands</code>\n\n"
        ),
        "tech_works": (
            "<b>⚙️ Technical works ⚙️</b>\n"
            "<b>Attention!</b> At the moment, the AI part of the bot is not working\n"
        ),
        "welcome_tech_works": (
            "🤖 Hi! I'm a bot named barchy.\n"
            "I have some cool features in my arsenal!\n"
            "To find them out, type the command <code>/commands</code>\n\n"
            "<b>⚙️ Technical works ⚙️</b>\n"
            "<b>Attention!</b> At the moment, the AI part of the bot is not working\n"
        ),
        "commands": (
            "<b>Communication with AI</b>\n"
            "<code>/chat [request]</code> - communication with AI\n"
            "<code>/forget</code> - forget the whole dialog\n\n"
            "<b>Others commands</b>\n"
            "<code>/language</code> - change language\n"
        ),
        "translating_request": "",
        
        "request_processed": "Your request is being processed...",
        
        "forget_clear": "Conversation history has been cleared!",
        
        "just_chat": "Please specify text after the /chat command",
        
        "show_original_lang": "Show original",
    },
    
    "pl": {
        "change_language": "Język:",
        
        "change_language_succesfully": "Język został zmieniony!",
        
        "welcome_text": (
            "🤖 Cześć, jestem botem o imieniu barchy.\n"
            "Mam kilka fajnych funkcji w swoim arsenale!\n"
            "Aby je znaleźć, wpisz polecenie <code>/commands</code>\n\n"
        ),
        "tech_works": (
            "<b>⚙️ Prace techniczne ⚙️</b>\n"
            "<b>Uwaga!</b> W tej chwili część AI bota nie działa\n"
        ),
        "welcome_tech_works": (
            "🤖 Cześć, jestem botem o imieniu barchy.\n"
            "Mam kilka fajnych funkcji w swoim arsenale!\n"
            "Aby je znaleźć, wpisz polecenie <code>/commands</code>\n\n"
            "<b>⚙️ Prace techniczne ⚙️</b>\n"
            "<b>Uwaga!</b> W tej chwili część AI bota nie działa\n"
        ),
        "commands": (
            "<b>Komunikacja z AI</b>\n"
            "<code>/chat [zapyt]</code> - kominikacja z AI\n"
            "<code>/forget</code> - zapomnieć o całym dialogu\n\n"
            "<b>Pozostałe funkcje</b>\n"
            "<code>/language</code> - zmienić język\n"
        ),
        "translating_request": "Tłumaczenie zapytania...",
        
        "request_processed": "Twoje zapytanie jest przetwarzane...",
        
        "translating_text": "Tłumaczenie...",
        
        "forget_clear": "Historia rozmowy została wyczyszczona!",
        
        "just_chat": "Należy podać tekst po poleceniu /chat",
        
        "show_original_lang": "Pokaż oryginał",
    },
    "none": "Выбери язык"
}

language_keyboard = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(text="🇷🇺 Русский", callback_data="ru"),
        InlineKeyboardButton(text="🇺🇦 Українська", callback_data="ua")
    ],
    [
        InlineKeyboardButton(text="🇬🇧 English", callback_data="en"),
        InlineKeyboardButton(text="🇵🇱 Polski", callback_data="pl")
    ]
])

memes_keyboard = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(text="⬅️ Назад", callback_data="prev_meme"),
        InlineKeyboardButton(text="➡️ Вперёд", callback_data="next_meme")
    ],
    [
        InlineKeyboardButton(text="📤 Отправить свой мем", callback_data="send_meme")
    ]
])

show_original_keyboard = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(text="Show original", callback_data="show_original")
    ]
])