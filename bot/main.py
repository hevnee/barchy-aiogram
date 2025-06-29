from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from config import BotConfigs
from middlewares import CommandLoggingMiddleware, CallbackLoggerMiddleware
from handlers import register_handlers
from handlers.ai_commands import text_generator, process_queue
from handlers.dick import giveaway_check
from utils import logging
import asyncio

bot = Bot(
    token=BotConfigs.TOKEN,
    default=DefaultBotProperties(
        parse_mode=ParseMode.HTML
    )
)
dp = Dispatcher()

async def main():
    register_handlers(dp)
    logging.info("Bot has been started!")
    await text_generator.initialize()
    logging.info(f"Model *{BotConfigs.MODEL_NAME}* has been sucessfully loaded and is ready to go!")
    asyncio.create_task(process_queue(bot))
    asyncio.create_task(giveaway_check(bot))
    dp.message.middleware(CommandLoggingMiddleware())
    dp.callback_query.middleware(CallbackLoggerMiddleware())
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())