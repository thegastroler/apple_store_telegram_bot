from aiogram.filters import Command, Text
from aiogram.types import CallbackQuery, LabeledPrice, Message
from aiogram.utils.keyboard import InlineKeyboardBuilder
from config import TelegramSettings
from dependency_injector.wiring import Provide, inject
from use_cases import SqlaCategoriesRepository, SqlaUsersRepository
from use_cases.container import SqlaRepositoriesContainer

from . import router
from .callback_factories import CategoryCallbackFactory
from filters import AdminFilter

@router.message(AdminFilter(), Command("ban_user"))
@inject
async def cmd_start(
    message: Message,
    use_case: SqlaUsersRepository = Provide[SqlaRepositoriesContainer.users_repository],
):
    """
    Забанить пользователя
    """
    user_id = message.text.replace("/ban_user ", "")
    """добавить отправку id пользователя с пересланного сообщения"""
    try:
        user_id = int(user_id)
    except ValueError:
        user_id = None
        return await message.answer("Невалидный id!")
    await use_case.ban_user(user_id)
    await message.answer("Пользователь добавлен в бан-лист")
