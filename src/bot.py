import asyncio
import logging

from aiogram import Bot, Dispatcher

import handlers
from config import TelegramSettings
from middleware import UserDataCallbackMiddleware
from use_cases import container
from worker import app

logging.basicConfig(level=logging.INFO)
bot = Bot(token=TelegramSettings().token, parse_mode="HTML")


async def init_container():
    container.wire(packages=[handlers], modules=[app, UserDataCallbackMiddleware])


async def main():
    await init_container()
    dp = Dispatcher()
    from handlers import router

    dp.include_router(router)
    dp.callback_query.outer_middleware(UserDataCallbackMiddleware())
    dp.message.middleware(UserDataCallbackMiddleware())
    await dp.start_polling(bot)
    # from worker.app import scheduled_task
    # await scheduled_task()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit) as e:
        pass
