from aiogram.types import Message, LabeledPrice, PreCheckoutQuery, ContentType
from aiogram.dispatcher.filters import Command
from bot import dp, bot
from config import TelegramSettings


prices = [LabeledPrice(label='Ноутбук', amount=1000000)]

@dp.message_handler(Command("start"))
async def cmd_start(message: Message):
    await message.answer("Hello!")


@dp.message_handler(Command("dice"))
async def cmd_dice(message: Message):
    await message.answer_dice(emoji="🎲")


@dp.message_handler(Command("buy"))
async def cmd_buy(message: Message):
    await bot.send_invoice(
        chat_id=message.chat.id,
        title='Laptop',
        description='Игровой ноутбук',
        provider_token=TelegramSettings().pay_token,
        currency='RUB',
        need_email=True,
        need_shipping_address=True,
        is_flexible=True,
        prices=prices,
        payload='some_invoice'
    )


@dp.pre_checkout_query_handler(lambda query: True)
async def pre_checkout_query_handler(pre_checkout_query: PreCheckoutQuery):
    await bot.answer_pre_checkout_query(pre_checkout_query.id, ok=True)


@dp.message_handler(content_types=ContentType.SUCCESSFUL_PAYMENT)
async def successful_payment_handler(message: Message):
    await message.answer('Платеж прошел успешно!')
