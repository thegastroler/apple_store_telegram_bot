from aiogram import F
from aiogram.filters import Command, Text
from aiogram.types import (CallbackQuery, LabeledPrice, Message,
                           PreCheckoutQuery, ShippingOption, ShippingQuery)
from bot import bot
from config import TelegramSettings
from dependency_injector.wiring import Provide, inject
from use_cases import SqlaCategoriesRepository, SqlaUsersRepository
from use_cases.container import SqlaRepositoriesContainer
from use_cases.shopping_list import SqlaShoppingListRepository

from . import router
from .callback_factories import CategoryCallbackFactory

STANDART_SHIPPING = ShippingOption(
    id='standart',
    title='Стандартная доставка',
    prices=[LabeledPrice(
        label='Стандартная доставка',
        amount=50000)
    ])
FAST_SHIPPING = ShippingOption(
    id='fast',
    title='Быстрая доставка',
    prices=[LabeledPrice(
        label='Быстрая доставка',
        amount=200000)
    ])

PRICES = [LabeledPrice(label='Ноутбук', amount=10000)]


@router.callback_query(Text("pay"))
async def pay(
    callback: CallbackQuery,
    use_case: SqlaShoppingListRepository = Provide[SqlaRepositoriesContainer.shopping_list_repository]
    ):
    await callback.message.answer_invoice(
        title='title',
        description='description',
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
