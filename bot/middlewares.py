from aiogram.types import Message, CallbackQuery
from aiogram.dispatcher.middlewares.base import BaseMiddleware
import logging


class CommandLoggingMiddleware(BaseMiddleware):
    async def __call__(self, handler, event, data):
        if isinstance(event, Message) and event.text and event.text.startswith('/'):
            user = event.from_user
            command = event.text.split()[0]
            logging.debug(f"{user.full_name} (ID: {user.id}, @{user.username or 'no_username'}) used command {command!r}")
        
        return await handler(event, data)


class CallbackLoggerMiddleware(BaseMiddleware):
    async def __call__(self, handler, event, data):
        if isinstance(event, CallbackQuery):
            user = event.from_user
            callback_data = event.data
            logging.debug(f"{user.full_name} (ID: {user.id}, @{user.username or 'no_username'}) clicked callback {callback_data!r}")

        return await handler(event, data)