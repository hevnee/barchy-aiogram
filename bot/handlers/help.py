from aiogram import Router, types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from services import user_save, get_lang
from states import LangStates
from functools import partial
from keyboards import language_keyboard
from locales import SELECTED_LANGUAGE

router = Router()

async def is_not_forwarded(message: types.Message) -> bool:
    return not message.forward_date


@router.message(Command("help"), is_not_forwarded)
async def help_command(message: types.Message, state: FSMContext):
    user = message.from_user
    user_save(user)

    lang = get_lang(user.id)
    if lang is None:
        await state.set_state(LangStates.command)
        await state.update_data(command=partial(help_command, message, state))
        return await message.reply(text=SELECTED_LANGUAGE["none"], reply_markup=language_keyboard)

    await message.reply(SELECTED_LANGUAGE[lang]["help_text"])