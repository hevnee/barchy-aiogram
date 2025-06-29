from aiogram import Dispatcher

from .start import router as start_router
from .help import router as help_router
from .language import router as language_router
from .ai_commands import router as chat_router
from .history import router as history_router
from .dick import router as dick_router

def register_handlers(dp: Dispatcher):
    dp.include_routers(
        start_router,
        help_router,
        language_router,
        chat_router,
        history_router,
        dick_router,
    )