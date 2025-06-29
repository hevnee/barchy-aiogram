from aiogram import Router, types, Bot
from aiogram.filters import Command, CommandObject
from aiogram.fsm.context import FSMContext
from services import user_save, get_lang, database, cursor
from states import LangStates
from functools import partial
from keyboards import language_keyboard, giveaway_keyboard
from locales import SELECTED_LANGUAGE, SUPPORTED_LANGUAGES
from datetime import datetime
import json, random, asyncio, logging

router = Router()

async def is_not_forwarded(message: types.Message) -> bool:
    return not message.forward_date


# giveaway handler
@router.callback_query(lambda c: c.data == "giveaway_participate")
async def giveaway_handler(callback_query: types.CallbackQuery):
    user = callback_query.from_user
    user_save(user)
    chat_id = callback_query.message.chat.id

    giveaway = cursor.execute("SELECT * FROM giveaways WHERE chat_id = ? AND status = ?", (chat_id, "going_on")).fetchone()

    lang = user.language_code
    if lang not in SUPPORTED_LANGUAGES:
        lang_dict = SUPPORTED_LANGUAGES["ru"]
    else:
        lang_dict = SELECTED_LANGUAGE[lang]
    
    if not giveaway:
        return await callback_query.answer(lang_dict["giveaway_no_longer_active"])

    if user.id == giveaway[0]:
        return await callback_query.answer(lang_dict["giveaway_creator_cannot_join"])

    users = giveaway[3]

    if not users:
        giveaways_user = json.dumps([user.id])
        cursor.execute("UPDATE giveaways SET users = ? WHERE chat_id = ?", (giveaways_user, chat_id))
        database.commit()
        return await callback_query.answer(lang_dict["giveaway_join_success"])

    users = json.loads(users)
    if user.id in users:
        return await callback_query.answer(lang_dict["giveaway_already_joined"])

    users.append(user.id)
    users = json.dumps(users)
    cursor.execute("UPDATE giveaways SET users = ? WHERE chat_id = ?", (users, chat_id))
    database.commit()

    await callback_query.answer(lang_dict["giveaway_join_success"])


# /dick command
@router.message(Command("dick"), is_not_forwarded)
async def dick_command(message: types.Message, state: FSMContext):
    user = message.from_user
    user_save(user)
    
    lang = get_lang(user.id)
    if lang is None:
        await state.set_state(LangStates.command)
        await state.update_data(command=partial(dick_command, message, state))
        return await message.reply(text=SELECTED_LANGUAGE["none"], reply_markup=language_keyboard)
    
    lang_dict = SELECTED_LANGUAGE[lang]

    chat_id = message.chat.id
    if user.id == message.chat.id:
        return await message.reply(text=lang_dict["command_private"])

    cursor.execute("SELECT active_chats, last_used, size FROM dick_game WHERE user_id = ?", (user.id,))
    active_chats, last_used, dick_size = cursor.fetchone()

    if active_chats is None:
        cursor.execute("UPDATE dick_game SET active_chats = ? WHERE user_id = ?", (json.dumps([chat_id]), user.id))
        database.commit()
    else:
        chats_list = json.loads(active_chats)
        if chat_id not in chats_list:
            chats_list.append(chat_id)
            cursor.execute("UPDATE dick_game SET active_chats = ? WHERE user_id = ?", (json.dumps(chats_list), user.id))
            database.commit()

    current_time = datetime.now().timestamp()

    if last_used > current_time:
        return await message.reply(lang_dict["dick_already_played"].format(value=dick_size))

    growth = random.randint(-5, 10)
    dick_size += growth
    cursor.execute("UPDATE dick_game SET size = ?, last_used = ? WHERE user_id = ?", (dick_size, current_time+43200, user.id))
    database.commit()

    if growth >= 0:
        change_text = lang_dict["dick_grew"].format(value=abs(growth))
    else:
        change_text = lang_dict["dick_shrank"].format(value=abs(growth))

    text = (
        f"{change_text}\n"
        f"{lang_dict['dick_equal_now'].format(value=dick_size)}."
    )
    await message.reply(text)


# /top_dick command
@router.message(Command("top_dick"), is_not_forwarded)
async def chat_top_dick_command(message: types.Message, state: FSMContext):
    user = message.from_user
    user_save(user)
    chat_id = message.chat.id
    lang = get_lang(user.id)
    if lang is None:
        await state.set_state(LangStates.command)
        await state.update_data(command=partial(chat_top_dick_command, message, state))
        return await message.reply(text=SELECTED_LANGUAGE["none"], reply_markup=language_keyboard)

    lang_dict = SELECTED_LANGUAGE[lang]

    if user.id == chat_id:
        return await message.reply(
            f"{lang_dict['command_private']}",
        )

    users = cursor.execute("""
        SELECT users.full_name, dick_game.size, dick_game.active_chats 
        FROM users 
        INNER JOIN dick_game ON users.user_id = dick_game.user_id
        ORDER BY -dick_game.size
    """).fetchall()

    filtered = []
    for full_name, size, raw_chats in users:
        try:
            chats_list = json.loads(raw_chats or "[]")
        except Exception:
            chats_list = []
        if chat_id in chats_list:
            filtered.append((full_name, size))
    if not filtered:
        return await message.reply(lang_dict["dick_nobody_played"])

    top = min(10, len(filtered))
    text = lang_dict["top_dick_chat_title"].format(count=top)
    for index in range(top):
        text += f"{index+1} | <b>{filtered[index][0]}</b> — <b>{filtered[index][1]}</b> {lang_dict['cm']}.\n"

    await message.reply(text)


# /global_top_dick command
@router.message(Command("global_top_dick"), is_not_forwarded)
async def global_top_dick_command(message: types.Message, state: FSMContext):
    user = message.from_user
    user_save(user)
    chat_id = message.chat.id
    lang = get_lang(user.id)
    if lang is None:
        await state.set_state(LangStates.command)
        await state.update_data(command=partial(global_top_dick_command, message, state))
        return await message.reply(text=SELECTED_LANGUAGE["none"], reply_markup=language_keyboard)

    lang_dict = SELECTED_LANGUAGE[lang]
    
    if user.id != chat_id:
        return await message.reply(lang_dict["top_dick_global_private"])

    users = cursor.execute("""
        SELECT users.full_name, dick_game.size, dick_game.active_chats 
        FROM users 
        INNER JOIN dick_game ON users.user_id = dick_game.user_id
        ORDER BY -dick_game.size
    """).fetchall()

    text = lang_dict["top_dick_global_title"].format(count=len(users))
    for user in range(len(users)):
        text += f"{user+1} | <b>{users[user][0]}</b> — <b>{users[user][1]}</b> {lang_dict['cm']}.\n"

    await message.reply(text)


# /giveaway command
@router.message(Command("giveaway"))
async def giveaway_command(message: types.Message, command: CommandObject, state: FSMContext):
    user = message.from_user
    user_save(user)

    lang = get_lang(user.id)
    if lang is None:
        await state.set_state(LangStates.command)
        await state.update_data(command=partial(giveaway_command, message, command, state))
        return await message.reply(text=SELECTED_LANGUAGE["none"], reply_markup=language_keyboard)
    
    lang_dict = SELECTED_LANGUAGE[lang]
    chat_id = message.chat.id
    if user.id == chat_id:
        return await message.reply(lang_dict["command_private"])

    args = command.args
    if not args:
        return await message.reply(lang_dict["requires_number"])
    args = args.split()

    dick_size = cursor.execute("SELECT size FROM dick_game WHERE user_id = ?", (user.id,)).fetchone()[0]
    giveaway_size = abs(int(args[0]))

    if giveaway_size <= 0:
        return await message.reply(lang_dict["invalid_amount"])

    if dick_size == 0 or dick_size < giveaway_size:
        return await message.reply(lang_dict["giveaway_insufficient_dick"])
    
    check = cursor.execute("SELECT * FROM giveaways WHERE chat_id = ? AND status = ?", (chat_id, "going_on")).fetchone()
    if check is not None:
        return await message.reply(lang_dict["giveaway_already_ongoing"])
    
    dick_size -= giveaway_size
    cursor.execute("UPDATE dick_game SET size = ? WHERE user_id = ?", (dick_size, user.id))
    database.commit()

    timestamp = datetime.now().timestamp()
    try: 
        time = int(args[1])
        if time <= 0:
            return await message.reply(lang_dict["giveaway_invalid_time_low"])
        elif time > 48:
            return await message.reply(lang_dict["giveaway_invalid_time_high"])
    except:
        time = 24
    cursor.execute(
        "INSERT INTO giveaways (creator_id, chat_id, size, timestamp_start, timestamp_end, status) VALUES (?, ?, ?, ?, ?, ?)", 
        (user.id, chat_id, giveaway_size, timestamp, timestamp + time * 3600, "going_on")
    )
    database.commit()
    text = lang_dict["giveaway_created"].format(
        user_id=user.id,
        full_name=user.full_name,
        size=giveaway_size,
        hours=time
    )
    msg = await message.reply(text, reply_markup=giveaway_keyboard(lang_dict))
    cursor.execute("UPDATE giveaways SET message_id = ? WHERE chat_id = ? AND status = ?", (msg.message_id, chat_id, "going_on"))
    database.commit()


# /tranfer command
@router.message(Command("transfer"), is_not_forwarded)
async def transfer_command(message: types.Message, command: CommandObject, state: FSMContext, bot: Bot):
    user = message.from_user
    user_save(user)
    lang = get_lang(user.id)
    if lang is None:
        await state.set_state(LangStates.command)
        await state.update_data(command=partial(transfer_command, message, command, state, bot))
        return await message.reply(text=SELECTED_LANGUAGE["none"], reply_markup=language_keyboard)

    lang_dict = SELECTED_LANGUAGE[lang]
    chat_id = message.chat.id
    if user.id == chat_id:
        return await message.reply(f"{lang_dict['command_private']}")

    args = command.args
    if not args:
        return await message.reply(lang_dict["transfer_no_args"])
    args = args.split()

    transfer_user = args[0]
    try:
        if int(transfer_user) == user.id:
            return await message.reply(lang_dict["transfer_self"])
    except:
        if user.username in (transfer_user, transfer_user.strip("@")):
            return await message.reply(lang_dict["transfer_self"])
    
    transfer_user = cursor.execute("""
        SELECT users.user_id, users.username, users.full_name, dick_game.size, dick_game.active_chats
        FROM users
        INNER JOIN dick_game ON users.user_id = dick_game.user_id
        WHERE users.user_id = ? OR users.username = ?
        """, (transfer_user, transfer_user.strip("@") or transfer_user,)).fetchone()
    
    if not transfer_user:
        return await message.reply(lang_dict["transfer_user_not_found"])

    size = cursor.execute("SELECT size FROM dick_game WHERE user_id = ?", (user.id,)).fetchone()[0]

    transfer_user_chats = json.loads(transfer_user[4])
    if chat_id not in transfer_user_chats:
        return await message.reply(lang_dict["transfer_recipient_not_in_chat"])

    transfer_user_size = transfer_user[3]
    try:
        transfer_size = abs(int(args[1]))
    except:
        return await message.reply(lang_dict["transfer_invalid_amount"])

    if size < transfer_size:
        return await message.reply(lang_dict["transfer_insufficient_dick"])

    size -= transfer_size
    transfer_user_size += transfer_size
    cursor.execute("UPDATE dick_game SET size = ? WHERE user_id = ?", (transfer_user_size, transfer_user[0]))
    cursor.execute("UPDATE dick_game SET size = ? WHERE user_id = ?", (size, user.id))
    database.commit()

    mention_transfer_user = f"<a href='tg://user?id={transfer_user[0]}'>{transfer_user[2]}</a>"
    mention = f"<a href='tg://user?id={user.id}'>{user.full_name}</a>"
    text = lang_dict["transfer_success_sender"].format(
        amount=transfer_size,
        mention=mention_transfer_user,
        remaining=size
    )
    await message.reply(text)
    text = lang_dict["transfer_success_receiver"].format(
        mention=mention_transfer_user,
        sender_mention=mention,
        amount=transfer_size,
        new_amount=transfer_user_size
    )
    await bot.send_message(chat_id, text)


# giveaway checker
async def giveaway_check(bot: Bot):
    while True:
        await asyncio.sleep(10)
        try:
            timestamp_now = datetime.now().timestamp()
            giveaways = cursor.execute(
                "SELECT * FROM giveaways WHERE status = ? AND timestamp_end <= ?", 
                ("going_on", timestamp_now)
            ).fetchall()
            
            if not giveaways:
                continue

            for index in range(len(giveaways)):
                giveaway = giveaways[index]
                chat_id = giveaway[1]
                users = giveaway[3]
                
                creator_lang = cursor.execute("SELECT lang FROM users WHERE user_id = ?", (giveaway[0],)).fetchone()[0]
                lang_dict = SELECTED_LANGUAGE[creator_lang]
                
                if users is None:
                    await bot.send_message(
                        chat_id=chat_id,
                        text=lang_dict["giveaway_no_participants"],
                    )
                    continue
                users = json.loads(users)
                
                winner_id = random.choice(users)
                
                winner = cursor.execute("""
                    SELECT users.full_name, dick_game.size
                    FROM users
                    INNER JOIN dick_game ON users.user_id = dick_game.user_id
                    WHERE users.user_id = ?
                    """, (winner_id,)).fetchone()
                
                giveaway_size = giveaway[4]
                winner_size = winner[1]
                winner_size += giveaway_size
                
                cursor.execute("UPDATE dick_game SET size = ? WHERE user_id = ?", (winner_size, winner_id))
                cursor.execute("UPDATE giveaways SET status = ?, winner = ? WHERE chat_id = ?", ("completed", winner_id, chat_id))
                database.commit()

                mention = f"<a href='tg://user?id={winner_id}'>{winner[0]}</a>"
                text = (
                    lang_dict["giveaway_winner_announcement"].format(
                        giveaway_size=giveaway_size,
                        mention=mention,
                        winner_size=winner_size
                    )
                )

                await bot.send_message(
                    chat_id=chat_id,
                    text=text,
                    reply_to_message_id=giveaway[2]
                )
        except Exception as e:
            logging.error(f"{e}")
            continue