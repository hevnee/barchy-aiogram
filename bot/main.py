from configs.settings import *
from services.generator import TextGenerator

logging.basicConfig(level=logging.INFO)
memory_storage = {}
text_generator = TextGenerator()

bot = Bot(token=TOKEN)
dp = Dispatcher()

class RequestQueue:
    def __init__(self):
        self.queue = asyncio.Queue()
        self.processing = False
        self.active_tasks = 0

request_queue = RequestQueue()

async def cleanup_memory():
    current_time = datetime.now().timestamp()
    to_delete = [k for k, v in memory_storage.items() if current_time - v["timestamp"] > MEMORY_DURATION]
    for k in to_delete:
        del memory_storage[k]

# show_original button handler
@dp.callback_query(lambda c: c.data == "show_original")
async def show_original_option(callback_query: types.CallbackQuery):
    await callback_query.answer()
    user_id = callback_query.from_user.id
    lang = get_lang(user_id)
    
    message_text = callback_query.message.text
    cursor_logs.execute("SELECT answer_original FROM requests WHERE answer_translation = ?", (message_text,))
    result = cursor_logs.fetchone()

    if result is None:
        await callback_query.message.reply("ERROR")
        return

    if lang is None:
        show_translation_keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text=select_language["ru"]["show_translation_lang"], callback_data="show_translation")]
        ])
    else:
        show_translation_keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text=select_language[lang]["show_translation_lang"], callback_data="show_translation")]
        ])
    await callback_query.message.edit_text(
        text=result[0],
        reply_markup=show_translation_keyboard
    )

# show_translation button handler
@dp.callback_query(lambda c: c.data == "show_translation")
async def show_translation_option(callback_query: types.CallbackQuery):
    await callback_query.answer()
    user_id = callback_query.from_user.id
    lang = get_lang(user_id)
    
    message_text = callback_query.message.text
    cursor_logs.execute("SELECT answer_translation FROM requests WHERE answer_original = ?", (message_text,))
    result = cursor_logs.fetchone()
    
    if result is None:
        await callback_query.message.reply("ERROR")
        return

    if lang is None:
        show_original_keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text=select_language["ru"]["show_original_lang"], callback_data="show_original")]
        ])
    else:
        show_original_keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text=select_language[lang]["show_original_lang"], callback_data="show_original")]
        ])
    await callback_query.message.edit_text(
        text=result[0],
        reply_markup=show_original_keyboard
    )

# ai
async def process_queue():
    while True:
        task = await request_queue.queue.get()

        try:
            message, args, processing_msg, time, lang = task
            chat_id = message.chat.id

            await asyncio.sleep(0.3)

            await bot.edit_message_text(
                chat_id=chat_id,
                message_id=processing_msg.message_id,
                text=select_language[lang]["request_processed"]
            )

            user_message = f"User: {args}"
            memory_storage[chat_id]["history"].append(user_message)
            history = "\n".join(memory_storage[chat_id]["history"])
            prompt = f"{history}\nAssistant:"

            #logging.info(f"\nПолный промпт:\n{prompt}")

            try:
                start = times.time()
                full_response = await text_generator.generate_text_async(prompt)
                response = full_response[len(prompt):].strip() if full_response.startswith(prompt) else full_response

                memory_storage[chat_id]["history"].append(f"{response}")

                cursor_logs.execute("UPDATE requests SET answer_original = ? WHERE time = ?", (response, time))
                database_logs.commit()

                if lang == "en":
                    pass
                else:
                    await bot.edit_message_text(
                        chat_id=chat_id,
                        message_id=processing_msg.message_id,
                        text=select_language[lang]["translating_text"]
                    )
                    try:
                        url = "http://localhost:5000/translate"
                        data = {
                            "q": response,
                            "source": "en",
                            "target": lang,
                            "format": "text"
                        }
                        get_response = requests.post(url, json=data)
                        response = get_response.json().get("translatedText")
                    except:
                        await bot.edit_message_text(
                            chat_id=chat_id,
                            message_id=processing_msg.message_id,
                            text=select_language[lang]["translator_not_working"]
                        )
                        return
                end = times.time()
                avg = round(end-start, 2)
                cursor_logs.execute("UPDATE requests SET answer_translation = ?, action_time = ? WHERE time = ?", (response, avg, time))
                database_logs.commit()

                if len(response) > 4096:
                    chunks = [response[i:i+4096] for i in range(0, len(response), 4096)]
                    for chunk in chunks:
                        await message.reply(chunk)
                else:
                    if lang == "en":
                        await bot.edit_message_text(
                            chat_id=chat_id,
                            message_id=processing_msg.message_id,
                            text=response,
                        )
                    else:
                        show_original_keyboard = InlineKeyboardMarkup(inline_keyboard=[
                            [InlineKeyboardButton(text=select_language[lang]["show_original_lang"], callback_data="show_original")]
                        ])
                        await bot.edit_message_text(
                            chat_id=chat_id,
                            message_id=processing_msg.message_id,
                            text=response,
                            reply_markup=show_original_keyboard
                        )

                #logging.info(response)

            except Exception as e:
                await message.reply(f"ERROR: {str(e)}")
                logging.error(f"ERROR: {e}")

        finally:
            request_queue.queue.task_done()

async def on_startup():
    logging.info(' Bot has been started! 🍪')
    await text_generator.initialize()
    logging.info(" Model has been sucessfully loaded and is ready to go!")
    
    asyncio.create_task(process_queue())

# change_language handler
@dp.callback_query()
async def callback_handler(callback_query: types.CallbackQuery):
    data = callback_query.data
    user_id = callback_query.from_user.id
    time = datetime.now().strftime("%d.%m.%Y %H:%M:%S:%f")
    if data in languages:
        user_save(user_id, callback_query.from_user.username, time)
        cursor_logs.execute("UPDATE users_logs SET lang = ? WHERE user_id = ?", (data, user_id))
        database_logs.commit()
        await callback_query.message.answer(text=select_language[data]["change_language_succesfully"])

    await callback_query.answer()



# /start
@dp.message(Command('start'))
async def start_command(message: Message):
    user_id = message.from_user.id
    time = datetime.now().strftime("%d.%m.%Y %H:%M:%S:%f")

    user_save(user_id, message.from_user.username, time)
    lang = get_lang(user_id)

    if lang is not None:
        await message.reply(select_language[lang]["welcome_text"], parse_mode=ParseMode.HTML)
    elif lang is None:
        await change_language(message)

# /language      
@dp.message(Command('language'))
async def change_language(message: Message):
    user_id = message.from_user.id
    time = datetime.now().strftime("%d.%m.%Y %H:%M:%S:%f")

    user_save(user_id, message.from_user.username, time)
    lang = get_lang(user_id)

    if lang is not None:
        await message.reply(select_language[lang]["change_language"], reply_markup=language_keyboard)
    else:
        await message.reply(select_language["none"], reply_markup=language_keyboard)

# /commands
@dp.message(Command('commands'))
async def commands_command(message: Message):
    user_id = message.from_user.id
    time = datetime.now().strftime("%d.%m.%Y %H:%M:%S:%f")

    user_save(user_id, message.from_user.username, time)
    lang = get_lang(user_id)

    if lang is not None:
        await message.reply(select_language[lang]["commands"], parse_mode=ParseMode.HTML)
    elif lang is None:
        await change_language(message)

# /forget
@dp.message(Command('forget'))
async def forget_command(message: Message):
    user_id = message.from_user.id
    time = datetime.now().strftime("%d.%m.%Y %H:%M:%S:%f")

    user_save(user_id, message.from_user.username, time)
    lang = get_lang(user_id)

    if lang is None:
        await change_language(message)
        return
    
    chat_id = message.chat.id
    if chat_id in memory_storage:
        del memory_storage[chat_id]
    await message.reply(select_language[lang]["forget_clear"])

# /chat
@dp.message(Command('chat'))
async def chat_command(message: Message):
    user_id = message.from_user.id
    time = datetime.now().strftime("%d.%m.%Y %H:%M:%S:%f")
    
    user_save(user_id, message.from_user.username, time)
    lang = get_lang(user_id)

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
            await message.reply(select_language[lang]["just_chat"])
            return

        if lang == "en":
            processing_msg = await message.reply(select_language[lang]["request_processed"])
        else:
            try:
                processing_msg = await message.reply(select_language[lang]["translating_request"])
                url = "http://localhost:5000/translate"
                data = {
                    "q": args,
                    "source": lang,
                    "target": "en",
                    "format": "text"
                }
                response = requests.post(url, json=data)
                args = response.json().get("translatedText")
            except:
                await bot.edit_message_text(
                    chat_id=chat_id,
                    message_id=processing_msg.message_id,
                    text=select_language[lang]["translator_not_working"]
                )
                return

        cursor_logs.execute("INSERT OR IGNORE INTO requests (user_id, username, request, time) VALUES (?, ?, ?, ?)", 
                      (user_id, message.from_user.username, request, time))
        database_logs.commit()

        await request_queue.queue.put((message, args, processing_msg, time, lang))

        position_in_queue = request_queue.queue.qsize()
        text = f'{select_language[lang]["position_in_queue"] + str(position_in_queue)}.' 
        await bot.edit_message_text(
            chat_id=chat_id,
            message_id=processing_msg.message_id,
            text=text
        )

    elif lang is None:
        await change_language(message)

async def main():
    await on_startup()
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())

database_logs.close()