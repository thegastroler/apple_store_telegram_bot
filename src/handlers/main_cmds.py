from aiogram import F
from aiogram.filters import Command, Text
from aiogram.types import (CallbackQuery, InlineKeyboardButton, LabeledPrice,
                           Message, PreCheckoutQuery, ShippingOption,
                           ShippingQuery)
from aiogram.utils.keyboard import InlineKeyboardBuilder
from bot import bot
from config import TelegramSettings
from dependency_injector.wiring import Provide, inject
from use_cases import SqlaCategoriesRepository, SqlaUsersRepository
from use_cases.container import SqlaRepositoriesContainer

from . import router
from .callback_factories import CategoryCallbackFactory

PRICES = [LabeledPrice(label='Ноутбук', amount=10000)]

def main_keyboard():
    """
    Клавиатура главного меню
    """
    builder = InlineKeyboardBuilder()
    builder.add(
        InlineKeyboardButton(
            text="🏪 К товарам",
            callback_data="items"),
        InlineKeyboardButton(
            text="🛒 Корзина",
            callback_data="bucket"),
    )
    return builder.as_markup()


@router.message(Command("start"))
@inject
async def cmd_start(message: Message, use_case: SqlaUsersRepository = Provide[SqlaRepositoriesContainer.users_repository]):
    """
    Приветствие
    """
    user = await use_case.create(message.chat.id, message.chat.username)
    if user and user.is_admin:
        await message.answer("Привет админ!")
    else:
        await message.answer("Привет!")


@router.message(Command("main"))
async def cmd_main(message: Message):
    """
    Главное меню
    """
    await message.answer(
        "🏠 Домашняя страница",
        reply_markup=main_keyboard()
    )


@router.callback_query(Text("items"))
@inject
async def items(callback: CallbackQuery, use_case: SqlaCategoriesRepository = Provide[SqlaRepositoriesContainer.category_repository]):
    """
    Категории
    """
    categories = await use_case.get_all()
    builder = InlineKeyboardBuilder()
    for i in categories:
        builder.button(
            text=i.name, callback_data=CategoryCallbackFactory(id=i.id, name=i.name)
        )
    builder.button(
        text="« Назад в главное меню", callback_data="back_to_main"
    )
    builder.adjust(1)
    await callback.message.edit_text(
        "🏠 Категории",
        reply_markup=builder.as_markup()
    )


@router.callback_query(Text("back_to_main"))
async def back_to_main(callback: CallbackQuery):
    """
    Кнопка "Назад в главное меню из Категорий"
    """
    await callback.message.edit_text(
        "🏠 Домашняя страница",
        reply_markup=main_keyboard()
    )


@router.message(Command("buy"))
async def cmd_buy(message: Message):
    await message.answer_invoice(
        title='Laptop',
        description='Игровой ноутбук',
        provider_token=TelegramSettings().pay_token,
        currency='RUB',
        need_email=True,
        need_shipping_address=True,
        is_flexible=True,
        prices=PRICES,
        payload='some_invoice'
    )
