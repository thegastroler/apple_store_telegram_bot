from aiogram.filters import Command
from aiogram.types import Message

from . import router


@router.message(Command("dice"))
async def cmd_dice(message: Message):
    """
    Бросить кость
    """
    await message.answer_dice(emoji="🎲")
