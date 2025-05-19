from configs.settings import *

logging.basicConfig(level=logging.INFO)

bot = Bot(token=TOKEN)
dp = Dispatcher()

async def on_startup():
    logging.info('Bot has been started! 🍪')
    logging.info('Bot in technical work mode')

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

# /start
@dp.message(Command('start'))
async def start_command(message: Message):
    user_id = message.from_user.id
    time = datetime.now().strftime("%d.%m.%Y %H:%M:%S:%f")

    user_save(user_id, message.from_user.username, time)
    lang = get_lang(user_id)

    if lang is None:
        global command
        await change_language_command(message)
        command = start_command(message)
        return

    await message.reply(select_language[lang]["welcome_tech_works"], parse_mode=ParseMode.HTML)

# /language      
@dp.message(Command('language'))
async def change_language_command(message: Message):
    user_id = message.from_user.id
    time = datetime.now().strftime("%d.%m.%Y %H:%M:%S:%f")

    user_save(user_id, message.from_user.username, time)
    lang = get_lang(user_id)

    if lang is None:
        await message.reply(select_language["none"], reply_markup=language_keyboard)
        return

    await message.reply(select_language[lang]["change_language"], reply_markup=language_keyboard)

# change_language handler
@dp.callback_query()
async def callback_handler(callback_query: types.CallbackQuery):
    data = callback_query.data
    user_id = callback_query.from_user.id
    time = datetime.now().strftime("%d.%m.%Y %H:%M:%S:%f")
    user_save(user_id, callback_query.from_user.username, time)

    if data in languages:
        cursor_logs.execute("UPDATE users_logs SET lang = ? WHERE user_id = ?", (data, user_id))
        database_logs.commit()
        await callback_query.message.reply(text=select_language[data]["change_language_succesfully"])

        if "command" in globals():
            global command
            await command
            del command

    await callback_query.answer()

# /commands
@dp.message(Command('commands'))
async def commands_command(message: Message):
    user_id = message.from_user.id
    time = datetime.now().strftime("%d.%m.%Y %H:%M:%S:%f")

    user_save(user_id, message.from_user.username, time)
    lang = get_lang(user_id)
    
    if lang is None:
        global command
        await change_language_command(message)
        command = commands_command(message)
        return
    
    await message.reply(select_language[lang]["commands"], parse_mode=ParseMode.HTML)

# /chat
@dp.message(Command('chat'))
async def chat_command(message: Message):
    user_id = message.from_user.id
    time = datetime.now().strftime("%d.%m.%Y %H:%M:%S:%f")
    
    user_save(user_id, message.from_user.username, time)
    lang = get_lang(user_id)

    if lang is None:
        global command
        await change_language_command(message)
        command = chat_command(message)
        return

    await message.reply(select_language[lang]["tech_works"], parse_mode=ParseMode.HTML)

# /forget
@dp.message(Command('forget'))
async def forget_command(message: Message):
    user_id = message.from_user.id
    time = datetime.now().strftime("%d.%m.%Y %H:%M:%S:%f")

    user_save(user_id, message.from_user.username, time)
    lang = get_lang(user_id)
    
    if lang is None:
        global command
        await change_language_command(message)
        command = forget_command(message)
        return
    
    await message.reply(select_language[lang]["tech_works"], parse_mode=ParseMode.HTML)

async def main():
    await on_startup()
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())

database_logs.close()