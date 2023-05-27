import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.types import Message

from config import TelegramSettings

logging.basicConfig(level=logging.INFO)
bot = Bot(token=TelegramSettings().token)
dp = Dispatcher(bot)

async def main():
    from handlers import dp
    await dp.start_polling()


if __name__ == "__main__":
    asyncio.run(main())
