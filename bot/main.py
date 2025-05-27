from configs.settings import *
from services.generator import TextGenerator
from services.translate import *

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


#previous, reset, next buttons handler for /history command
@dp.callback_query(lambda c: c.data in ("prev_h", "reset_h", "next_h") and c.from_user.id == c.message.reply_to_message.from_user.id)
async def Hkeyboard_navigate_options(callback_query: types.CallbackQuery):
    await callback_query.answer()
    user = callback_query.from_user
    lang = get_lang(user)
    
    current_page, response = get_currpage_resp(user)
    if not response:
        return await callback_query.message.edit_text(SELECTED_LANGUAGE[lang]["you_have_no_request"], reply_markup=UHkeyboard(SELECTED_LANGUAGE, lang))

    data = callback_query.data
    if data == "prev_h":
        if current_page > 0:
            current_page -= 1
        else:
            if len(response) == 1:
                return
            current_page = len(response) - 1

    elif data == "reset_h":
        if current_page == 0:
            return
        current_page = 0

    elif data == "next_h":
        if len(response) == 1:
            return
        if current_page < len(response) - 1:
            current_page += 1
        else:
            current_page = 0

    update_history_position(current_page, user)
    text = texting(response, current_page, user)
    await callback_query.message.edit_text(
        text=text, 
        parse_mode=ParseMode.HTML, 
        reply_markup=Hkeyboard(
            current_page+1, 
            len(response), 
            response[current_page][2],
            SELECTED_LANGUAGE,
            lang
        )
    )


#show_original, show_translation buttons handler for /history command 
@dp.callback_query(lambda c: c.data in ("show_original_h", "show_translation_h") and c.from_user.id == c.message.reply_to_message.from_user.id)
async def Hkeyboard_translate_options(callback_query: types.CallbackQuery):
    await callback_query.answer()
    data = callback_query.data
    user = callback_query.from_user
    lang = get_lang(user)

    if data == "show_original_h":
        current_page, response = get_currpage_resp_original(user)
        if not response:        
            return await callback_query.message.edit_text(SELECTED_LANGUAGE[lang]["you_have_no_request"], reply_markup=UHkeyboard(SELECTED_LANGUAGE, lang))
        text = texting(response, current_page, user)
        keyboard = Hkeyboard_translation

    elif data == "show_translation_h":
        current_page, response = get_currpage_resp(user)
        if not response:
            return await callback_query.message.edit_text(SELECTED_LANGUAGE[lang]["you_have_no_request"], reply_markup=UHkeyboard(SELECTED_LANGUAGE, lang))
        
        text = texting(response, current_page, user)
        keyboard = Hkeyboard

    await callback_query.message.edit_text(
            text=text, 
            parse_mode=ParseMode.HTML, 
            reply_markup=keyboard(
                current_page+1, 
                len(response), 
                response[current_page][2],
                SELECTED_LANGUAGE, 
                lang
            )
        )


#delete requests handler for /history command
@dp.callback_query(lambda c: c.data in ("delete_this_request_h", "delete_all_h") and c.from_user.id == c.message.reply_to_message.from_user.id)
async def delete_request_option(callback_query: types.CallbackQuery):
    await callback_query.answer()
    data = callback_query.data
    user = callback_query.from_user
    lang = get_lang(user)
    current_page, response = get_currpage_resp(user)
    if not response:
        return await callback_query.message.edit_text(SELECTED_LANGUAGE[lang]["you_have_no_request"], reply_markup=UHkeyboard(SELECTED_LANGUAGE, lang))
    
    if data == "delete_all_h":
        await callback_query.message.reply(SELECTED_LANGUAGE[lang]["r_u_s_del_all"], reply_markup=Ckeyboard("yes_all", SELECTED_LANGUAGE, lang))
    else:
        await callback_query.message.reply(SELECTED_LANGUAGE[lang]["r_u_s_del_this"], reply_markup=Ckeyboard("yes_this_request", SELECTED_LANGUAGE, lang))


#confirmation delete requests handler for /history command
@dp.callback_query(lambda c: c.data in ("yes_all", "no_c", "yes_this_request"))
async def confirmation_del(callback_query: types.CallbackQuery):
    await callback_query.answer()
    data = callback_query.data
    chat_id = callback_query.message.chat.id
    user = callback_query.from_user
    msg_id = callback_query.message.message_id

    if data == "yes_all":
        cursor.execute("DELETE FROM request_history WHERE user_id = ?", (user.id,))
        database.commit()
        update_history_position(0, user)
        await bot.delete_message(chat_id, msg_id)

    elif data == "yes_this_request":
        current_page, response = get_currpage_resp(user)
        if len(response) == 1:
            cursor.execute("DELETE FROM request_history WHERE user_id = ? AND timestamp = ?", (user.id, response[current_page][3]))
            database.commit()
        elif len(response) > 1:
            cursor.execute("DELETE FROM request_history WHERE user_id = ? AND timestamp = ?", (user.id, response[current_page][3]))
            database.commit()
            if current_page == 0:
                current_page += 1
            else:
                current_page -= 1
        update_history_position(current_page, user)
        await bot.delete_message(chat_id, msg_id)

    else:
        await bot.delete_message(chat_id, msg_id)


#update button handler for /history command
@dp.callback_query(lambda c: c.data == "update_h" and c.from_user.id == c.message.reply_to_message.from_user.id)
async def update_history_option(callback_query: CallbackQuery):
    await callback_query.answer()
    user = callback_query.from_user
    lang = get_lang(user)
    
    current_page, response = get_currpage_resp(user)
    if not response:
        return

    text = texting(response, current_page, user)
    await callback_query.message.edit_text(
        text=text, 
        parse_mode=ParseMode.HTML, 
        reply_markup=Hkeyboard(
            current_page+1, 
            len(response), 
            response[current_page][2],
            SELECTED_LANGUAGE, lang
        )
    )


#show original and show translation handlers for /chat command
@dp.callback_query(lambda c: c.data in ("show_original", "show_translation") and c.from_user.id == c.message.reply_to_message.from_user.id)
async def show_options(callback_query: types.CallbackQuery):
    await callback_query.answer()
    data = callback_query.data
    user = callback_query.from_user
    lang = get_lang(user)
    message_text = callback_query.message.text

    if data == "show_original":
        result = cursor.execute("SELECT response_original FROM request_history WHERE response_translation = ? AND user_id = ?", (message_text, user.id)).fetchone()
        if result is None:
            return await callback_query.message.edit_text(SELECTED_LANGUAGE[lang]["request_has_been_deleted"])
        keyboard = STkeyboard(SELECTED_LANGUAGE, lang)
        await callback_query.message.edit_text(
            text=result[0],
            parse_mode=ParseMode.HTML,
            reply_markup=keyboard
        )

    else:
        result = cursor.execute("SELECT response_translation FROM request_history WHERE response_original = ? AND user_id = ?", (message_text, user.id)).fetchone()
        if result is None:
            return await callback_query.message.edit_text(SELECTED_LANGUAGE[lang]["request_has_been_deleted"])

        keyboard = SOkeyboard(SELECTED_LANGUAGE, lang)
        await callback_query.message.edit_text(
            text=result[0],
            parse_mode=ParseMode.HTML,
            reply_markup=keyboard
        )


#language changer handler for /language command
@dp.callback_query(lambda c: c.data in SUPPORTED_LANGUAGES and c.from_user.id == c.message.reply_to_message.from_user.id)
async def change_language_handler(callback: types.CallbackQuery):
    await callback.answer()
    data = callback.data
    user = callback.from_user

    cursor.execute("UPDATE users SET lang = ? WHERE user_id = ?", (data, user.id))
    database.commit()
    await callback.message.reply(text=SELECTED_LANGUAGE[data]["change_language_succesfully"])

    if user.id in user_command:
        await user_command[user.id]()
        del user_command[user.id]


# /start command
@dp.message(Command("start"))
async def start_command(message: Message):
    user = message.from_user
    await user_save(user, datetime.now().strftime("%d.%m.%Y %H:%M:%S"))

    lang = get_lang(user)
    if lang is None:
        user_command[user.id] = partial(start_command, message)
        return await change_language(message)

    await message.reply(SELECTED_LANGUAGE[lang]["welcome_text"], parse_mode=ParseMode.HTML)


# /help command
@dp.message(Command("help"))
async def help_command(message: Message):
    user = message.from_user
    await user_save(user, datetime.now().strftime("%d.%m.%Y %H:%M:%S"))
    
    lang = get_lang(user)
    if lang is None:
        user_command[user.id] = partial(help_command, message)
        return await change_language(message)

    await message.reply(SELECTED_LANGUAGE[lang]["commands"], parse_mode=ParseMode.HTML)


# /language command
@dp.message(Command("language"))
async def change_language(message: Message):
    user = message.from_user
    await user_save(user, datetime.now().strftime("%d.%m.%Y %H:%M:%S"))

    lang = get_lang(user)
    if lang is None:
        await message.reply(SELECTED_LANGUAGE["none"], reply_markup=language_keyboard)
    else:
        await message.reply(SELECTED_LANGUAGE[lang]["change_language"], reply_markup=language_keyboard)


# /chat command
@dp.message(Command("chat"))
async def chat_command(message: Message):
    user = message.from_user
    date = datetime.now().strftime("%d.%m.%Y %H:%M")
    timestamp = datetime.now().timestamp()
    await user_save(user, datetime.now().strftime("%d.%m.%Y %H:%M:%S"))

    lang = get_lang(user)
    if lang is None:
        user_command[user.id] = partial(chat_command, message)
        return await change_language(message)

    chat_id = message.chat.id
    await cleanup_memory()
    if user.id not in memory_storage:
        memory_storage[user.id] = {
            "history": deque(maxlen=MAX_HISTORY_LENGTH),
            "timestamp": datetime.now().timestamp()
        }

    memory_storage[user.id]["timestamp"] = datetime.now().timestamp()
    request = message.text.split('/chat', 1)[1].strip()
    if not request:
        return await message.reply(SELECTED_LANGUAGE[lang]["just_chat"])

    cursor.execute("INSERT OR IGNORE INTO request_history (user_id, username, request_original, date, timestamp) VALUES (?, ?, ?, ?, ?)", 
        (user.id, message.from_user.username, request, date, timestamp))
    database.commit()

    if lang == "en":
        processing_msg = await message.reply(SELECTED_LANGUAGE[lang]["request_processed"])
    else:
        try:
            processing_msg = await message.reply(SELECTED_LANGUAGE[lang]["translating_request"])

            request = translate_request(request, lang)
        except:
            return await bot.edit_message_text(
                chat_id=chat_id,
                message_id=processing_msg.message_id,
                text=SELECTED_LANGUAGE[lang]["translator_not_working"]
            )

    cursor.execute("UPDATE request_history SET request_translation = ? WHERE timestamp = ?", (request, timestamp))
    database.commit()
    await request_queue.queue.put((message, request, processing_msg, timestamp, lang))
    position_in_queue = request_queue.queue.qsize()
    await bot.edit_message_text(
        chat_id=chat_id,
        message_id=processing_msg.message_id,
        text=f"{SELECTED_LANGUAGE[lang]['position_in_queue'] + str(position_in_queue)}."
    )

#AI
async def process_queue():
    while True:
        await asyncio.sleep(0.5)
        task = await request_queue.queue.get()

        try:
            message, request, processing_msg, timestamp, lang = task
            chat_id = message.chat.id

            await asyncio.sleep(0.3)

            await bot.edit_message_text(
                chat_id=chat_id,
                message_id=processing_msg.message_id,
                text=SELECTED_LANGUAGE[lang]["request_processed"]
            )

            user_message = f"User: {request}"
            memory_storage[chat_id]["history"].append(user_message)
            history = "\n".join(memory_storage[chat_id]["history"])
            prompt = f"{history}\nAssistant:"

            #logging.info(f"\nFull prompt:\n{prompt}")

            try:
                full_response = await text_generator.generate_text_async(prompt)
                response = full_response[len(prompt):].strip() if full_response.startswith(prompt) else full_response

                memory_storage[chat_id]["history"].append(f"{response}\n")

                cursor.execute("UPDATE request_history SET response_original = ? WHERE timestamp = ?", (response, timestamp))
                database.commit()

                await bot.edit_message_text(
                    chat_id=chat_id,
                    message_id=processing_msg.message_id,
                    text=SELECTED_LANGUAGE[lang]["translating_text"]
                )
                try:
                    response = translate_response(response, lang)
                except:
                    return await bot.edit_message_text(
                        chat_id=chat_id,
                        message_id=processing_msg.message_id,
                        text=SELECTED_LANGUAGE[lang]["translator_not_working"]
                    )
                        
                cursor.execute("UPDATE request_history SET response_translation = ? WHERE timestamp = ?", (response, timestamp))
                database.commit()

                if len(response) > 4096:
                    chunks = [response[i:i+4096] for i in range(0, len(response), 4096)]
                    for chunk in chunks:
                        await message.reply(chunk, parse_mode=ParseMode.HTML)
                else:
                    await bot.edit_message_text(
                        chat_id=chat_id,
                        message_id=processing_msg.message_id,
                        text=response,
                        reply_markup=SOkeyboard(SELECTED_LANGUAGE, lang),
                        parse_mode=ParseMode.HTML
                    )

            except Exception as e:
                await message.reply(f"ERROR: {e}")
                logging.error(f"ERROR: {e}")

        finally:
            request_queue.queue.task_done()


# /history command
@dp.message(Command("history"))
async def history_command(message: Message):
    user = message.from_user
    await user_save(user, datetime.now().strftime("%d.%m.%Y %H:%M:%S"))

    lang = get_lang(user)
    if lang is None:
        user_command[user.id] = partial(history_command, message)
        return await change_language(message)

    current_page, response = get_currpage_resp(user)
    if not response:        
        return await message.reply(SELECTED_LANGUAGE[lang]["you_have_no_request"], reply_markup=UHkeyboard(SELECTED_LANGUAGE, lang))
    text = texting(response, current_page, user)
    keyboard = Hkeyboard(current_page+1, len(response), response[current_page][2], SELECTED_LANGUAGE, lang)
    await message.reply(text=text, parse_mode=ParseMode.HTML, reply_markup=keyboard)


# /forget command
@dp.message(Command("forget"))
async def forget_command(message: Message):
    user = message.from_user
    await user_save(user, datetime.now().strftime("%d.%m.%Y %H:%M:%S"))
    
    lang = get_lang(user)
    if lang is None:
        user_command[user.id] = partial(forget_command, message)
        return await change_language(message)

    if user.id in memory_storage:
        del memory_storage[user.id]
    await message.reply(SELECTED_LANGUAGE[lang]["forget_clear"])


async def cleanup_memory():
    current_time = datetime.now().timestamp()
    to_delete = [k for k, v in memory_storage.items() if current_time - v["timestamp"] > MEMORY_DURATION]
    for k in to_delete:
        del memory_storage[k]

async def on_startup():
    logging.debug("Bot has been started!")
    await text_generator.initialize()
    logging.info("Model has been sucessfully loaded and is ready to go!")
    asyncio.create_task(process_queue())

async def main():
    await on_startup()
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())

database.close()