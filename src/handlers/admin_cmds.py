from aiogram.filters import Command
from aiogram.types import Message
from dependency_injector.wiring import Provide, inject
from use_cases import SqlaUsersRepository
from use_cases.container import SqlaRepositoriesContainer

from . import router
from filters import AdminFilter


@router.message(AdminFilter(), Command("ban"))
@inject
async def ban(
    message: Message,
    use_case: SqlaUsersRepository = Provide[SqlaRepositoriesContainer.users_repository],
):
    """
    Забанить пользователя
    """
    username = message.text.split(" ")
    if len(username) == 2:
        username = username[-1]
        returned_username = await use_case.ban_user(username)
        if returned_username and returned_username == username:
            await message.answer("Пользователь добавлен в бан-лист")
        else:
            await message.answer("Пользователь не найден!")
    else:
        return await message.answer("Введите имя пользователя!")


@router.message(AdminFilter(), Command("unban"))
@inject
async def unban(
    message: Message,
    use_case: SqlaUsersRepository = Provide[SqlaRepositoriesContainer.users_repository],
):
    """
    Разбанить пользователя
    """
    username = message.text.split(" ")
    if len(username) == 2:
        username = username[-1]
        returned_username = await use_case.unban_user(username)
        if returned_username and returned_username == username:
            await message.answer("Пользователь исключен из бан-листа")
        else:
            await message.answer("Пользователь не найден!")
    else:
        return await message.answer("Введите имя пользователя!")
