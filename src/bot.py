import asyncio
import logging

from aiogram import Bot, Dispatcher

import handlers
from config import TelegramSettings
from middleware import IsBannedCallbackMiddleware
from use_cases import container
from worker import app

logging.basicConfig(level=logging.INFO)
bot = Bot(token=TelegramSettings().token, parse_mode="HTML")


async def main():
    container.wire(packages=[handlers], modules=[app])

    dp = Dispatcher()
    from handlers import router

    dp.include_router(router)
    dp.callback_query.outer_middleware(IsBannedCallbackMiddleware())
    dp.message.middleware(IsBannedCallbackMiddleware())
    await dp.start_polling(bot)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit) as e:
        pass
