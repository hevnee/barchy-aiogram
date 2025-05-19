import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.enums import ParseMode
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from generator import TextGenerator
from aiogram.filters import Command
from aiogram.types import Message
from datetime import datetime
from collections import deque
import settings as settings
import logging
import sqlite3
import requests
import time as times

logging.basicConfig(level=logging.INFO)

database = sqlite3.connect("logs.db")
cursor = database.cursor()

settings.create_tables()

MAX_HISTORY_LENGTH = 100
MEMORY_DURATION = 10000

bot = Bot(token=settings.TOKEN)
dp = Dispatcher()

memory_storage = {}

text_generator = TextGenerator()

class RequestQueue:
    def __init__(self):
        self.queue = asyncio.Queue()
        self.processing = False
        self.active_tasks = 0

request_queue = RequestQueue()

def users_logs(user_id, username, time):
    cursor.execute("INSERT OR IGNORE INTO users_logs (user_id, username, time) VALUES (?, ?, ?)", (user_id, username, time))
    database.commit()

async def cleanup_memory():
    current_time = datetime.now().timestamp()
    to_delete = [k for k, v in memory_storage.items() 
                if current_time - v["timestamp"] > MEMORY_DURATION]
    for k in to_delete:
        del memory_storage[k]

async def process_queue():
    while True:
        # Ждем новый запрос в очереди
        task = await request_queue.queue.get()
        
        try:
            # Получаем данные задачи
            message, args, processing_msg, time, lang = task
            chat_id = message.chat.id

            await asyncio.sleep(0.3)
            if lang == "en":
                pass
            else:
                await bot.edit_message_text(
                    chat_id=chat_id,
                    message_id=processing_msg.message_id,
                    text=settings.select_language[lang]["request_processed"]
                )
            
            # Обработка запроса
            user_message = f"User question (ONLY ONE QUESTION): {args}"
            memory_storage[chat_id]["history"].append(user_message)
            history = "\n".join(memory_storage[chat_id]["history"])
            prompt = f"{history}\nBot answer:"
            
            logging.info(f"\nПолный промпт:\n{prompt}")
            
            try:
                start = times.time()
                full_response = await text_generator.generate_text_async(prompt)
                new_response = full_response[len(prompt):].strip() if full_response.startswith(prompt) else full_response

                memory_storage[chat_id]["history"].append(f"{new_response}")

                cursor.execute("UPDATE requests SET answer_en = ? WHERE time = ?", (new_response, time))
                database.commit()

                if lang == "en":
                    pass
                else:
                    await bot.edit_message_text(
                        chat_id=chat_id,
                        message_id=processing_msg.message_id,
                        text=settings.select_language[lang]["translating_text"]
                    )
                    try:
                        url = "http://localhost:5000/translate"
                        data = {
                            "q": new_response,
                            "source": "en",
                            "target": lang,
                            "format": "text"
                        }
                        response = requests.post(url, json=data)
                        new_response = response.json().get("translatedText")
                    except:
                        await bot.edit_message_text(
                            chat_id=chat_id,
                            message_id=processing_msg.message_id,
                            text="Переводчик не включен"
                        )
                        return
                end = times.time()
                avg = round(end-start, 2)
                cursor.execute("UPDATE requests SET answer_ru = ?, action_time = ? WHERE time = ?", (new_response, avg, time))
                database.commit()

                if len(new_response) > 4096:  # Максимальная длина сообщения в Telegram
                    chunks = [new_response[i:i+4096] for i in range(0, len(new_response), 4096)]
                    for chunk in chunks:
                        await message.reply(chunk)
                else:
                    await bot.edit_message_text(
                            chat_id=chat_id,
                            message_id=processing_msg.message_id,
                            text=new_response
                        )

                logging.info(new_response)
                
            except Exception as e:
                await message.reply(f"ERROR: {str(e)}")
                logging.error(f"ERROR: {e}")
        
        finally:
            # Помечаем задачу как выполненную
            request_queue.queue.task_done()

async def on_startup():
    logging.info('Бот запущен!🍪')
    await text_generator.initialize()
    logging.info("Модель загружена и готова к работе!")

    # Запускаем обработчик очереди в фоне
    asyncio.create_task(process_queue())

# Оброботка выбора языка
@dp.callback_query()
async def callback_handler(callback_query: types.CallbackQuery):
    data = callback_query.data
    user_id = callback_query.from_user.id
    if data in settings.languages:
        cursor.execute("UPDATE users_logs SET lang = ? WHERE user_id = ?", (data, user_id))
        database.commit()
        await callback_query.message.answer(text=settings.select_language[data]["change_language_succesfully"])

    await callback_query.answer()  # обязательно вызываем, чтобы убрать "часики"

# /start
@dp.message(Command('start'))
async def start_command(message: Message):
    user_id = message.from_user.id
    time=datetime.now().strftime("%d.%m.%Y %H:%M:%S:%f")
    
    settings.saving(
        username=message.from_user.username,
        user_id=user_id,
        time=time,
    )
    lang = settings.get_lang(user_id)

    if lang is not None:
        await message.reply(settings.select_language[lang]["welcome_text"], parse_mode=ParseMode.HTML)
    elif lang is None:
        await change_language(message)

# /language
@dp.message(Command('language'))
async def change_language(message: Message):
    user_id = message.from_user.id
    time=datetime.now().strftime("%d.%m.%Y %H:%M:%S:%f")

    settings.saving(
        username=message.from_user.username,
        user_id=user_id,
        time=time,
    )
    lang = settings.get_lang(user_id)
    
    if lang is not None:
        await message.reply(settings.select_language[lang]["change_language"], reply_markup=settings.language_keyboard)
    else:
        await message.reply(settings.select_language["none"], reply_markup=settings.language_keyboard)

@dp.message(Command('commands'))
async def commands_command(message: Message):
    user_id = message.from_user.id
    time=datetime.now().strftime("%d.%m.%Y %H:%M:%S:%f")
    
    settings.saving(
        username=message.from_user.username,
        user_id=user_id,
        time=time,
    )
    lang = settings.get_lang(user_id)

    if lang is not None:
        await message.reply(settings.select_language[lang]["commands"], parse_mode=ParseMode.HTML)
    elif lang is None:
        await change_language(message)

@dp.message(Command('forget'))
async def forget_command(message: Message):
    user_id = message.from_user.id
    time=datetime.now().strftime("%d.%m.%Y %H:%M:%S:%f")
    
    settings.saving(
        username=message.from_user.username,
        user_id=user_id,
        time=time,
    )
    lang = settings.get_lang(user_id)

    if lang is not None:
        chat_id = message.chat.id
        if chat_id in memory_storage:
            del memory_storage[chat_id]
        await message.reply(settings.select_language[lang]["forget_clear"])
    elif lang is None:
        await change_language(message)

@dp.message(Command('chat'))
async def ai_command(message: Message):
    user_id = message.from_user.id
    time=datetime.now().strftime("%d.%m.%Y %H:%M:%S:%f")
    
    settings.saving(
        username=message.from_user.username,
        user_id=user_id,
        time=time,
    )
    lang = settings.get_lang(user_id)

    if lang is not None:
        await cleanup_memory()
        chat_id = message.chat.id
        if chat_id not in memory_storage:
            memory_storage[chat_id] = {
                "history": deque(maxlen=MAX_HISTORY_LENGTH),
                "timestamp": datetime.now().timestamp()
            }

        memory_storage[chat_id]["timestamp"] = datetime.now().timestamp()

        args = message.text.split('/chat', 1)[1].strip()
        request = args

        if not args:
            await message.reply(settings.select_language[lang]["just_chat"])
            return

        if lang == "en":
            processing_msg = await message.reply(settings.select_language[lang]["request_processed"])
        else:
            try:
                processing_msg = await message.reply(settings.select_language[lang]["translating_request"])
                url = "http://localhost:5000/translate"
                data = {
                    "q": args,
                    "source": "auto",
                    "target": "en",
                    "format": "text"
                }
                response = requests.post(url, json=data)
                args = response.json().get("translatedText")
            except:
                await bot.edit_message_text(
                    chat_id=chat_id,
                    message_id=processing_msg.message_id,
                    text="Переводчик не включен"
                )
                return

        cursor.execute("INSERT OR IGNORE INTO requests (user_id, username, request, time) VALUES (?, ?, ?, ?)", 
                      (user_id, message.from_user.username, request, time))
        database.commit()

        # Добавляем запрос в очередь
        await request_queue.queue.put((message, args, processing_msg, time, lang))

        position_in_queue = request_queue.queue.qsize()
        await asyncio.sleep(0.2)
        await bot.edit_message_text(
            chat_id=chat_id,
            message_id=processing_msg.message_id,
            text=f"Ваш запрос в очереди. Позиция: {position_in_queue}. Ожидайте обработки..."
        )

    elif lang is None:
        await change_language(message)

async def main():
    await on_startup()
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())

database.close()