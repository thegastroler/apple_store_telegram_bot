from aiogram import F
from aiogram.filters import Command, Text
from aiogram.types import (CallbackQuery, LabeledPrice, Message,
                           PreCheckoutQuery, ShippingOption, ShippingQuery)
from aiogram.utils.keyboard import InlineKeyboardBuilder
from bot import bot
from config import TelegramSettings
from dependency_injector.wiring import Provide, inject
from use_cases import SqlaCategoriesRepository, SqlaUsersRepository
from use_cases.container import SqlaRepositoriesContainer
from use_cases.orders import SqlaOrdersRepository
from use_cases.shopping_list import SqlaShoppingListRepository
from utils import price_converter

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


@router.callback_query(Text("pay"))
@inject
async def pay(
    callback: CallbackQuery,
    use_case: SqlaShoppingListRepository = Provide[SqlaRepositoriesContainer.shopping_list_repository]
    ):
    """
    Оплата корзины
    """
    user_id = callback.from_user.id
    shopping_list = await use_case.get_shopping_list(user_id)

    if not shopping_list.items:
        return

    prices = [
        LabeledPrice(label=i.name, amount=i.price*100) for i in shopping_list.items
    ]
    await callback.message.answer_invoice(
        title="Оплата заказа",
        description=f"Заказ №{shopping_list.order}",
        provider_token=TelegramSettings().pay_token,
        currency="RUB",
        need_email=True,
        need_shipping_address=True,
        need_name=True,
        need_phone_number=True,
        is_flexible=True,
        prices=prices,
        payload=shopping_list.order,
        photo_url="https://support.apple.com/library/content/dam/edam/applecare/images/en_US/gifting/giftcardscertificates/gift-cards-app-store-itunes.png",
    )
    await callback.answer()


@router.shipping_query(lambda query: True)
async def shipping_process(shipping: ShippingQuery):
    """
    Подтверждение доставки
    """
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
@inject
async def pre_checkout_process(
    pre_checkout: PreCheckoutQuery,
    use_case: SqlaOrdersRepository = Provide[
        SqlaRepositoriesContainer.orders_repository]
    ):
    """
    Подтверждение перед оплатой
    """
    order = pre_checkout.invoice_payload
    paid = await use_case.is_paid_order(order)
    if paid:
        return await bot.answer_pre_checkout_query(
            pre_checkout.id,ok=False, error_message="Ваш заказ уже оплачен!")
    await bot.answer_pre_checkout_query(pre_checkout.id, ok=True)


@router.message(F.content_type.in_({'successful_payment'}))
@inject
async def successful_payment(
    message: Message,
    use_case: SqlaOrdersRepository = Provide[
        SqlaRepositoriesContainer.orders_repository]
    ):
    """
    Оплата прошла успешно
    """
    order = message.successful_payment.invoice_payload
    name = message.successful_payment.order_info.name
    phone_number = message.successful_payment.order_info.phone_number
    email = message.successful_payment.order_info.email
    state = message.successful_payment.order_info.shipping_address.state
    city = message.successful_payment.order_info.shipping_address.city
    street_line1 = message.successful_payment.order_info.shipping_address.street_line1
    street_line2 = message.successful_payment.order_info.shipping_address.street_line2
    post_code = message.successful_payment.order_info.shipping_address.post_code
    data = {
        "name": name,
        "phone_number": phone_number,
        "email": email,
        "state": state,
        "city": city,
        "street_line1": street_line1,
        "street_line2": street_line2,
        "post_code": post_code,
    }
    await use_case.update_info_on_paid(order, data)
    await message.answer('Платеж прошел успешно!')
