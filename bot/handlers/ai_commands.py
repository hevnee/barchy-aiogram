from aiogram import Router, types, Bot
from aiogram.filters import Command, CommandObject
from aiogram.fsm.context import FSMContext
from services import TextGenerator, user_save, get_lang, cursor, database, translate_request, translate_response, search_web
from states import LangStates
from functools import partial
from keyboards import language_keyboard, change_style_keyboard
from locales import SELECTED_LANGUAGE
from keyboards import show_original_keyboard as SOK
from keyboards import show_translation_keyboard as STK
from collections import deque
from datetime import datetime
from config import BotConfigs
import asyncio, logging

router = Router()

class RequestQueue:
    def __init__(self):
        self.queue = asyncio.Queue()
        self.processing = False
        self.active_tasks = 0
request_queue = RequestQueue()

memory_storage = {}
text_generator = TextGenerator()

name = BotConfigs.BOT_NAME
styles = {
    "normal": f"<|im_start|>system\n{f'You are an AI assistant named {name}. ' if name is not None else ''}{BotConfigs.STYLE_NORMAL}<|im_end|>",
    "sarcastic": f"<|im_start|>system\n{f'You are an AI assistant named {name}. ' if name is not None else ''}{BotConfigs.STYLE_SARCASTIC}<|im_end|>",
    "wise": f"<|im_start|>system\n{f'You are an AI assistant named {name}. ' if name is not None else ''}{BotConfigs.STYLE_WISE}<|im_end|>",
    "bastard": f"<|im_start|>system\n{f'You are an AI assistant named {name}. ' if name is not None else ''}{BotConfigs.STYLE_BASTARD}<|im_end|>"
}

def get_style(user_id: int) -> str:
    data = cursor.execute("SELECT AI_style FROM users WHERE user_id = ?", (user_id,)).fetchone()[0]
    return styles[data]

def update_style(style: str, user_id: int) -> None:
    cursor.execute("UPDATE users SET AI_style = ? WHERE user_id = ?", (style, user_id))
    return database.commit()

async def is_not_forwarded(message: types.Message) -> bool:
    return not message.forward_date

async def cleanup_memory():
    current_time = datetime.now().timestamp()
    to_delete = [k for k, v in memory_storage.items() if current_time - v["timestamp"] > BotConfigs.MEMORY_DURATION * 60]
    for k in to_delete:
        del memory_storage[k]


@router.callback_query(lambda c: c.data in ("show_original", "show_translation") and c.from_user.id == c.message.reply_to_message.from_user.id)
async def show_options(callback_query: types.CallbackQuery):
    await callback_query.answer()
    data = callback_query.data
    user = callback_query.from_user
    lang = get_lang(user.id)
    message_text = callback_query.message.text

    if data == "show_original":
        result = cursor.execute("SELECT response_original FROM request_history WHERE response_translation = ? AND user_id = ?", (message_text, user.id)).fetchone()
        if result is None:
            return await callback_query.message.edit_text(SELECTED_LANGUAGE[lang]["request_has_been_deleted"])
        keyboard = STK(SELECTED_LANGUAGE[lang])
        await callback_query.message.edit_text(
            text=result[0],
            reply_markup=keyboard,
            parse_mode=None
        )

    else:
        result = cursor.execute("SELECT response_translation FROM request_history WHERE response_original = ? AND user_id = ?", (message_text, user.id)).fetchone()
        if result is None:
            return await callback_query.message.edit_text(SELECTED_LANGUAGE[lang]["request_has_been_deleted"])

        keyboard = SOK(SELECTED_LANGUAGE[lang])
        await callback_query.message.edit_text(
            text=result[0],
            reply_markup=keyboard,
            parse_mode=None
        )


@router.callback_query(lambda c: c.data in ("style_normal", "style_sarcastic", "style_wise", "style_bastard") and c.from_user.id == c.message.reply_to_message.from_user.id)
async def change_ai_style_handler(callback_query: types.CallbackQuery, bot: Bot):
    await callback_query.answer()
    user = callback_query.from_user
    lang = get_lang(user.id)
    await cleanup_memory()
    data = callback_query.data
    if data == "style_normal":
        update_style("normal", user.id)
    elif data == "style_sarcastic":
        update_style("sarcastic", user.id)
    elif data == "style_wise":
        update_style("wise", user.id)
    elif data == "style_bastard":
        update_style("bastard", user.id)
    await bot.edit_message_text(
        text=SELECTED_LANGUAGE[lang]["style_change_succesfully"],
        chat_id=callback_query.message.chat.id,
        message_id=callback_query.message.message_id
    )


@router.message(Command("style"), is_not_forwarded)
async def change_ai_style_command(message: types.Message, state: FSMContext):
    user = message.from_user
    user_save(user)
    
    lang = get_lang(user.id)
    if lang is None:
        await state.set_state(LangStates.command)
        await state.update_data(command=partial(change_ai_style_command, message, state))
        return await message.reply(text=SELECTED_LANGUAGE["none"], reply_markup=language_keyboard)
    
    chat_id = message.chat.id
    await cleanup_memory()
    timestamp = datetime.now().timestamp()
    style = get_style(user.id)
    if chat_id not in memory_storage:
        memory_storage[chat_id] = {
            "system_message": style,
            "history": deque(maxlen=BotConfigs.MAX_MEMORY_LENGTH),
            "timestamp": timestamp
        }
    memory_storage[chat_id]["system_message"] = style
    memory_storage[chat_id]["timestamp"] = timestamp
    
    lang_dict = SELECTED_LANGUAGE[lang]
    await message.reply(lang_dict["style_choose"], reply_markup=change_style_keyboard(lang_dict))


@router.message(Command("chat"), is_not_forwarded)
async def chat_command(message: types.Message, command: CommandObject, state: FSMContext, bot: Bot):
    user = message.from_user
    user_save(user)
    
    lang = get_lang(user.id)
    if lang is None:
        await state.set_state(LangStates.command)
        await state.update_data(command=partial(chat_command, message, command, state, bot))
        return await message.reply(text=SELECTED_LANGUAGE["none"], reply_markup=language_keyboard)

    chat_id = message.chat.id
    await cleanup_memory()
    timestamp = datetime.now().timestamp()
    style = get_style(user.id)
    if chat_id not in memory_storage:
        memory_storage[chat_id] = {
            "system_message": style,
            "history": deque(maxlen=BotConfigs.MAX_MEMORY_LENGTH),
            "timestamp": timestamp
        }
    memory_storage[chat_id]["system_message"] = style
    memory_storage[chat_id]["timestamp"] = timestamp

    user_request = command.args
    if not user_request:
        return await message.reply(SELECTED_LANGUAGE[lang]["just_chat"])

    cursor.execute("""
        INSERT INTO request_history (user_id, request_original, date, timestamp) 
        VALUES (?, ?, ?, ?)
        """, (user.id, user_request, datetime.now().strftime("%d.%m.%Y %H:%M"), timestamp))
    database.commit()
    
    if lang == "en":
        processing_msg = await message.reply(SELECTED_LANGUAGE[lang]["request_processed"])
        translated_request = user_request
    else:
        try:
            processing_msg = await message.reply(SELECTED_LANGUAGE[lang]["translating_request"])

            translated_request = translate_request(user_request, lang)
        except:
            return await bot.edit_message_text(
                chat_id=chat_id,
                message_id=processing_msg.message_id,
                text=SELECTED_LANGUAGE[lang]["translator_not_working"]
            )
        
    cursor.execute("UPDATE request_history SET request_translation = ? WHERE timestamp = ?", (translated_request, timestamp))
    database.commit()
    
    request = f"<|im_start|>user\n{translated_request}<|im_end|>"
    memory_storage[chat_id]["history"].append(request)
    
    await request_queue.queue.put((message, processing_msg, timestamp, lang))
    position_in_queue = request_queue.queue.qsize()
    await bot.edit_message_text(
        chat_id=chat_id,
        message_id=processing_msg.message_id,
        text=f"{SELECTED_LANGUAGE[lang]['position_in_queue'] + str(position_in_queue)}."
    )


@router.message(Command("chatsearch"), is_not_forwarded)
async def chat_search_command(message: types.Message, command: CommandObject, state: FSMContext, bot: Bot):
    user = message.from_user
    user_save(user)
    
    lang = get_lang(user.id)
    if lang is None:
        await state.set_state(LangStates.command)
        await state.update_data(command=partial(chat_search_command, message, command, state, bot))
        return await message.reply(text=SELECTED_LANGUAGE["none"], reply_markup=language_keyboard)

    chat_id = message.chat.id
    await cleanup_memory()
    timestamp = datetime.now().timestamp()
    style = get_style(user.id)
    if chat_id not in memory_storage:
        memory_storage[chat_id] = {
            "system_message": style,
            "history": deque(maxlen=BotConfigs.MAX_MEMORY_LENGTH),
            "timestamp": timestamp
        }
    memory_storage[chat_id]["system_message"] = style
    memory_storage[chat_id]["timestamp"] = timestamp

    lang_dict = SELECTED_LANGUAGE[lang]
    user_request = command.args
    if not user_request:
        return await message.reply(lang_dict["just_chat"])

    processing_msg = await message.reply(lang_dict["translating_request"])
    try:
        translated_request = translate_request(user_request, lang)
    except:
        return await bot.edit_message_text(
            chat_id=chat_id,
            message_id=processing_msg.message_id,
            text=lang_dict["translator_not_working"]
        )
    
    cursor.execute("""
        INSERT INTO request_history (user_id, request_original, request_translation, date, timestamp) 
        VALUES (?, ?, ?, ?, ?)
        """, (user.id, user_request, translated_request, datetime.now().strftime("%d.%m.%Y %H:%M"), timestamp))
    database.commit()
    
    await bot.edit_message_text(
        text=lang_dict["chatsearch_fetching_data"], 
        chat_id=chat_id, 
        message_id=processing_msg.message_id
    )
    try:
        internet_results = search_web(translated_request)
    except Exception as e:
        return await bot.edit_message_text(
            text=f"{e}",
            chat_id=chat_id,
            message_id=processing_msg.message_id
        )

    request = f"<|im_start|>system\nFor this answer, use the information below. Internet results:\n{internet_results}<|im_end|>\n<|im_start|>user\n{translated_request}<|im_end|>"
    memory_storage[chat_id]["history"].append(request)

    await request_queue.queue.put((message, processing_msg, timestamp, lang))
    position_in_queue = request_queue.queue.qsize()
    await bot.edit_message_text(
        chat_id=chat_id,
        message_id=processing_msg.message_id,
        text=f"{lang_dict['position_in_queue'] + str(position_in_queue)}."
    )


# AI
async def process_queue(bot: Bot):
    while True:
        await asyncio.sleep(0.5)
        task = await request_queue.queue.get()

        try:
            message, processing_msg, timestamp, lang = task
            chat_id = message.chat.id

            await asyncio.sleep(0.4)
            
            lang_dict = SELECTED_LANGUAGE[lang]
            await bot.edit_message_text(
                chat_id=chat_id,
                message_id=processing_msg.message_id,
                text=lang_dict["request_processed"]
            )
            
            history = "\n".join(memory_storage[chat_id]["history"])
            full_history = f"{memory_storage[chat_id]['system_message']}\n{history}"
            prompt = f"{full_history}\n<|im_start|>assistant\n"

            try:
                full_response = await text_generator.generate_text_async(prompt)
                response = full_response[len(prompt):].strip() if full_response.startswith(prompt) else full_response
                response = response.replace("<|im_end|>", "") if "<|im_end|>" in response else response

                memory_storage[chat_id]["history"].append(f"<|im_start|>assistant\n{response}<|im_end|>\n")

                cursor.execute("UPDATE request_history SET response_original = ? WHERE timestamp = ?", (response, timestamp))
                database.commit()

                await bot.edit_message_text(
                    chat_id=chat_id,
                    message_id=processing_msg.message_id,
                    text=lang_dict["translating_text"]
                )
                try:
                    response = translate_response(response, lang)
                except:
                    return await bot.edit_message_text(
                        chat_id=chat_id,
                        message_id=processing_msg.message_id,
                        text=lang_dict["translator_not_working"]
                    )
                        
                cursor.execute("UPDATE request_history SET response_translation = ? WHERE timestamp = ?", (response, timestamp))
                database.commit()

                if len(response) > 4096:
                    chunks = [response[i:i+4096] for i in range(0, len(response), 4096)]
                    for chunk in chunks:
                        await message.reply(chunk, parse_mode=None)
                else:
                    await bot.edit_message_text(
                        chat_id=chat_id,
                        message_id=processing_msg.message_id,
                        text=response,
                        reply_markup=SOK(SELECTED_LANGUAGE[lang]),
                        parse_mode=None
                    )

            except Exception as e:
                await message.reply(f"ERROR: {e}")
                logging.error(f"ERROR: {e}")

        finally:
            request_queue.queue.task_done()


@router.message(Command("forget"), is_not_forwarded)
async def forget_command(message: types.Message, state: FSMContext):
    user = message.from_user
    chat_id = message.chat.id
    user_save(user)
    
    lang = get_lang(user.id)
    if lang is None:
        await state.set_state(LangStates.command)
        await state.update_data(command=partial(forget_command, message, state))
        return await message.reply(text=SELECTED_LANGUAGE["none"], reply_markup=language_keyboard)

    if user.id in memory_storage:
        del memory_storage[chat_id]
    await message.reply(SELECTED_LANGUAGE[lang]["forget_clear"])