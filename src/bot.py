import asyncio
import logging

from aiogram import Bot, Dispatcher
from use_cases import container
from handlers import default_cmds

from config import TelegramSettings

logging.basicConfig(level=logging.INFO)
bot = Bot(token=TelegramSettings().token, parse_mode="HTML")


async def main():
    container.wire(modules=[default_cmds])
    dp = Dispatcher()
    from handlers import router
    dp.include_router(router)
    await dp.start_polling(bot)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit) as e:
        pass
