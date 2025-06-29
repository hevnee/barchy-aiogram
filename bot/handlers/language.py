from aiogram import Router, types, Bot
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from services import user_save, get_lang, database, cursor
from keyboards import language_keyboard
from locales import SUPPORTED_LANGUAGES, SELECTED_LANGUAGE

router = Router()

async def is_not_forwarded(message: types.Message) -> bool:
    return not message.forward_date


@router.callback_query(lambda c: c.data in SUPPORTED_LANGUAGES and c.from_user.id == c.message.reply_to_message.from_user.id)
async def language_handler(callback_query: types.CallbackQuery, state: FSMContext, bot: Bot):
    await callback_query.answer()
    user = callback_query.from_user
    
    lang = callback_query.data
    cursor.execute("UPDATE users SET lang = ? WHERE user_id = ?", (lang, user.id))
    database.commit()
    
    await bot.edit_message_text(
        text=SELECTED_LANGUAGE[lang]["change_language_succesfully"],
        chat_id=callback_query.message.chat.id,
        message_id=callback_query.message.message_id
    )

    data = await state.get_data()
    if data:
        command = data.get("command")
        await command()
        return await state.clear()


@router.message(Command("language"), is_not_forwarded)
async def language_command(message: types.Message):
    user = message.from_user
    user_save(user)

    lang = get_lang(user.id)
    if lang is None:
        await message.reply(text=SELECTED_LANGUAGE["none"], reply_markup=language_keyboard)
    else:
        await message.reply(
            text=SELECTED_LANGUAGE[lang]["choose_language"],
            reply_markup=language_keyboard
        )