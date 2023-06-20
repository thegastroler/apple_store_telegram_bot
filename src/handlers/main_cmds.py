from aiogram.filters import Command, Text
from aiogram.types import CallbackQuery, Message
from aiogram.utils.keyboard import InlineKeyboardBuilder
from dependency_injector.wiring import Provide, inject
from use_cases import SqlaCategoriesRepository, SqlaUsersRepository
from use_cases.container import SqlaRepositoriesContainer

from . import router
from .callback_factories import CategoryCallbackFactory


async def main_text() -> str:
    return (
        "Добро пожаловать в Apple Store Bot!\n\n"
        "Чтобы воспользоваться ботом, вам доступны следующие команды:\n\n"
        "/main - домашняя страница\n"
    )


async def admin_text() -> str:
    return (
        "\n<b>Admin</b>\n"
        "/ban {username} - добавить пользователя в бан-лист\n"
        "/unban {username} - исключить пользователя из бан-листа"
    )


@router.message(Command("start"))
@inject
async def cmd_start(
    message: Message,
    use_case: SqlaUsersRepository = Provide[SqlaRepositoriesContainer.users_repository],
):
    """
    Приветствие
    """
    user = await use_case.create(message.chat.id, message.chat.username)
    text = await main_text()
    if user and user.is_admin:
        admin = await admin_text()
        await message.answer(text + admin)
    else:
        await message.answer(text)


async def homepage(
    use_case: SqlaCategoriesRepository = Provide[
        SqlaRepositoriesContainer.category_repository
    ],
):
    categories = await use_case.get_all()
    builder = InlineKeyboardBuilder()
    for i in categories:
        builder.button(
            text=i.name, callback_data=CategoryCallbackFactory(id=i.id, name=i.name)
        )
    builder.button(text="🧺 Корзина", callback_data="shopping_list")
    builder.adjust(1)
    return builder


@router.message(Command("main"))
@inject
async def main(message: Message):
    """
    Главная страница
    """
    builder = await homepage()
    await message.answer("Apple store", reply_markup=builder.as_markup())


@router.callback_query(Text("home"))
async def back_to_main(callback: CallbackQuery):
    """
    Кнопка "На главную страницу"
    """
    builder = await homepage()
    await callback.message.edit_text("Apple store", reply_markup=builder.as_markup())
