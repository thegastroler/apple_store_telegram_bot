from aiogram import F, Router
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.filters import Command, Text
from aiogram.types import (LabeledPrice, Message, PreCheckoutQuery,
                           ShippingOption, ShippingQuery, InlineKeyboardButton, CallbackQuery)
from bot import bot
from config import TelegramSettings
from dependency_injector.wiring import Provide, inject
from use_cases.container import SqlaRepositoriesContainer
from use_cases import SqlaUsersRepository, SqlaCategorysRepository

router = Router()

PRICES = [LabeledPrice(label='Ноутбук', amount=10000)]
STANDART_SHIPPING = ShippingOption(id='standart', title='Стандартная доставка', prices=[LabeledPrice(label='Стандартная доставка', amount=25000)])
FAST_SHIPPING = ShippingOption(id='fast', title='Быстрая доставка', prices=[LabeledPrice(label='Быстрая доставка', amount=50000)])


@router.message(Command("start"))
@inject
async def cmd_start(message: Message, use_case: SqlaUsersRepository = Provide[SqlaRepositoriesContainer.users_repository]):
    user = await use_case.create(message.chat.id, message.chat.username)
    if user and user.is_admin:
        await message.answer("Привет админ!")
    else:
        await message.answer("Привет!")


@router.message(Command("menu"))
async def cmd_menu(message: Message):
    builder = InlineKeyboardBuilder()
    builder.add(
        InlineKeyboardButton(
            text="🏪 К товарам",
            callback_data="items"),
        InlineKeyboardButton(
            text="🛒 Корзина",
            callback_data="bucket"),
    )
    await message.answer(
        "🏠 Домашняя страница",
        reply_markup=builder.as_markup()
    )


@router.callback_query(Text("items"))
@inject
async def cmd_menu(callback: CallbackQuery, use_case: SqlaCategorysRepository = Provide[SqlaRepositoriesContainer.category_repository]):
    categories = await use_case.get_all()
    builder = InlineKeyboardBuilder()
    for i in categories:
        builder.add(
            InlineKeyboardButton(
                text=i.name,
                callback_data=f"category_{i.id}"))
    builder.adjust(1)
    await callback.message.edit_text(
        "🏠 Категории",
        reply_markup=builder.as_markup()
    )


@router.message(Command("dice"))
async def cmd_dice(message: Message):
    await message.answer_dice(emoji="🎲")


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


@router.shipping_query(lambda query: True)
async def shipping_process(shipping: ShippingQuery):
    if shipping.shipping_address.country_code != 'RU':
        await bot.answer_shipping_query(
            shipping.id,
            ok=False,
            error_message='Извините, доставка возможна только в пределах РФ.')
    else:
        await bot.answer_shipping_query(
            shipping.id,
            ok=True,
            shipping_options=[STANDART_SHIPPING, FAST_SHIPPING])


@router.pre_checkout_query(lambda query: True)
async def pre_checkout_process(pre_checkout: PreCheckoutQuery):
    await bot.answer_pre_checkout_query(pre_checkout.id, ok=True)


@router.message(F.content_type.in_({'successful_payment'}))
async def successful_payment(message: Message):
    await message.answer('Платеж прошел успешно!')
