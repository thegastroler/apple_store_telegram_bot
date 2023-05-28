from aiogram.filters import Command
from aiogram.types import (ContentType, LabeledPrice, Message,
                           PreCheckoutQuery, ShippingQuery, ShippingOption)
from config import TelegramSettings
from aiogram import Router, F
from bot import bot

router = Router()


PRICES = [LabeledPrice(label='Ноутбук', amount=10000)]
STANDART_SHIPPING = ShippingOption(id='standart', title='Стандартная доставка', prices=[LabeledPrice(label='Стандартная доставка', amount=25000)])
FAST_SHIPPING = ShippingOption(id='fast', title='Быстрая доставка', prices=[LabeledPrice(label='Быстрая доставка', amount=50000)])

@router.message(Command("start"))
async def cmd_start(message: Message):
    await message.answer("Hello!")


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
