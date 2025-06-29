from aiogram import Router, types, Bot
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from services import user_save, get_lang, database, cursor
from states import LangStates
from functools import partial
from keyboards import language_keyboard
from locales import SELECTED_LANGUAGE
from keyboards import history_show_original as HSO
from keyboards import history_show_translation as HST
from keyboards import update_history_keyboard as UHK
from keyboards import confirmation_keyboard as CK
from config import BotConfigs

router = Router()


def get_currpage_resp(user_id: int):
    current_page = cursor.execute("SELECT history_position FROM users WHERE user_id = ?", (user_id,)).fetchone()[0]
    response = cursor.execute("SELECT request_original, response_translation, date, timestamp FROM request_history WHERE user_id = ? ORDER BY rowid", (user_id,)).fetchall()
    return current_page, response

def get_currpage_resp_original(user_id: int):
    current_page = cursor.execute("SELECT history_position FROM users WHERE user_id = ?", (user_id,)).fetchone()[0]
    response = cursor.execute("SELECT request_translation, response_original, date, timestamp FROM request_history WHERE user_id = ? ORDER BY rowid", (user_id,)).fetchall()
    return current_page, response

def update_history_position(current_page, user_id: int):
    cursor.execute("UPDATE users SET history_position = ? WHERE user_id = ?", (current_page, user_id))
    database.commit()

def history_text(response, current_page, user) -> str:
    mention = f"<a href='tg://user?id={user.id}'>{user.full_name}</a>"
    return f"{mention}: {response[current_page][0]}\n\n<b>{BotConfigs.BOT_NAME if BotConfigs.BOT_NAME is not None else 'AI'}</b>: {response[current_page][1]}"

async def is_not_forwarded(message: types.Message) -> bool:
    return not message.forward_date


#previous, reset, next buttons handler
@router.callback_query(lambda c: c.data in ("prev_h", "reset_h", "next_h") and c.from_user.id == c.message.reply_to_message.from_user.id)
async def Hkeyboard_navigate_options(callback_query: types.CallbackQuery):
    await callback_query.answer()
    user = callback_query.from_user
    lang = get_lang(user.id)
    
    current_page, response = get_currpage_resp(user.id)
    if not response:
        return await callback_query.message.edit_text(SELECTED_LANGUAGE[lang]["you_have_no_request"], reply_markup=UHK(SELECTED_LANGUAGE[lang]))

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

    update_history_position(current_page, user.id)
    text = history_text(response, current_page, user)
    await callback_query.message.edit_text(
        text=text, 
        reply_markup=HSO(
            current_page+1, 
            len(response), 
            response[current_page][2],
            SELECTED_LANGUAGE,
            lang
        )
    )


#show_original, show_translation buttons handler
@router.callback_query(lambda c: c.data in ("show_original_h", "show_translation_h") and c.from_user.id == c.message.reply_to_message.from_user.id)
async def Hkeyboard_translate_options(callback_query: types.CallbackQuery):
    await callback_query.answer()
    data = callback_query.data
    user = callback_query.from_user
    lang = get_lang(user.id)

    if data == "show_original_h":
        current_page, response = get_currpage_resp_original(user.id)
        if not response:        
            return await callback_query.message.edit_text(SELECTED_LANGUAGE[lang]["you_have_no_request"], reply_markup=UHK(SELECTED_LANGUAGE[lang]))
        text = history_text(response, current_page, user)
        keyboard = HST

    elif data == "show_translation_h":
        current_page, response = get_currpage_resp(user.id)
        if not response:
            return await callback_query.message.edit_text(SELECTED_LANGUAGE[lang]["you_have_no_request"], reply_markup=UHK(SELECTED_LANGUAGE[lang]))
        
        text = history_text(response, current_page, user)
        keyboard = HSO

    await callback_query.message.edit_text(
            text=text, 
            reply_markup=keyboard(
                current_page+1, 
                len(response), 
                response[current_page][2],
                SELECTED_LANGUAGE, 
                lang
            )
        )


#delete requests handler
@router.callback_query(lambda c: c.data in ("delete_this_request_h", "delete_all_h") and c.from_user.id == c.message.reply_to_message.from_user.id)
async def delete_request_option(callback_query: types.CallbackQuery):
    await callback_query.answer()
    data = callback_query.data
    user = callback_query.from_user
    lang = get_lang(user.id)
    current_page, response = get_currpage_resp(user.id)
    if not response:
        return await callback_query.message.edit_text(SELECTED_LANGUAGE[lang]["you_have_no_request"], reply_markup=UHK(SELECTED_LANGUAGE[lang]))
    
    if data == "delete_all_h":
        await callback_query.message.reply(SELECTED_LANGUAGE[lang]["r_u_s_del_all"], reply_markup=CK("yes_all", SELECTED_LANGUAGE[lang]))
    else:
        await callback_query.message.reply(SELECTED_LANGUAGE[lang]["r_u_s_del_this"], reply_markup=CK("yes_this_request", SELECTED_LANGUAGE[lang]))


#confirmation delete requests handler
@router.callback_query(lambda c: c.data in ("yes_all", "no_c", "yes_this_request"))
async def confirmation_del(callback_query: types.CallbackQuery, bot: Bot):
    await callback_query.answer()
    data = callback_query.data
    chat_id = callback_query.message.chat.id
    user = callback_query.from_user
    msg_id = callback_query.message.message_id

    if data == "yes_all":
        cursor.execute("DELETE FROM request_history WHERE user_id = ?", (user.id,))
        database.commit()
        update_history_position(0, user.id)
        await bot.delete_message(chat_id, msg_id)

    elif data == "yes_this_request":
        current_page, response = get_currpage_resp(user.id)
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
        update_history_position(current_page, user.id)
        await bot.delete_message(chat_id, msg_id)

    else:
        await bot.delete_message(chat_id, msg_id)


#update button handler
@router.callback_query(lambda c: c.data == "update_h" and c.from_user.id == c.message.reply_to_message.from_user.id)
async def update_history_option(callback_query: types.CallbackQuery):
    await callback_query.answer()
    user = callback_query.from_user
    lang = get_lang(user.id)
    
    current_page, response = get_currpage_resp(user.id)
    if not response:
        return

    text = history_text(response, current_page, user)
    await callback_query.message.edit_text(
        text=text, 
        reply_markup=HSO(
            current_page+1, 
            len(response), 
            response[current_page][2],
            SELECTED_LANGUAGE, lang
        )
    )


@router.message(Command("history"), is_not_forwarded)
async def history_command(message: types.Message, state: FSMContext):
    user = message.from_user
    user_save(user)

    lang = get_lang(user.id)
    if lang is None:
        await state.set_state(LangStates.command)
        await state.update_data(command=partial(history_command, message, state))
        return await message.reply(text=SELECTED_LANGUAGE["none"], reply_markup=language_keyboard)

    current_page, response = get_currpage_resp(user.id)
    if not response:        
        return await message.reply(SELECTED_LANGUAGE[lang]["you_have_no_request"], reply_markup=UHK(SELECTED_LANGUAGE[lang]))
    text = history_text(response, current_page, user)
    keyboard = HSO(current_page+1, len(response), response[current_page][2], SELECTED_LANGUAGE, lang)
    await message.reply(text=text, reply_markup=keyboard)