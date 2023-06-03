from aiogram.types import CallbackQuery
from aiogram.filters import Command, Text
from aiogram.types import Message
from aiogram.utils.keyboard import InlineKeyboardBuilder, InlineKeyboardMarkup, InlineKeyboardButton
from dependency_injector.wiring import Provide, inject
from use_cases import SqlaCategoriesRepository, SqlaItemsRepository, SqlaShoppingListRepository
from use_cases.container import SqlaRepositoriesContainer
from utils import price_converter

from . import router
from .callback_factories import (CategoryCallbackFactory,
                                  ItemIdCallbackFactory,
                                  ItemIndexCategoryCallbackFactory,
                                  ItemIndexStorageCallbackFactory)
from utils import make_order


@router.callback_query(Text("shopping_list"))
@inject
async def shopping_list(
    callback: CallbackQuery,
    use_case: SqlaShoppingListRepository = Provide[SqlaRepositoriesContainer.shopping_list_repository]
    ):
    """
    Корзина
    """
    user_id = callback.from_user.id
    shopping_list = await use_case.get_shopping_list(user_id)

    builder = InlineKeyboardBuilder()

    if not shopping_list.items:
        builder.button(text="« Назад в главное меню", callback_data="back_to_main")
        builder.button(text="🏪 К покупкам", callback_data="items")
        builder.adjust(1)
        return await callback.message.edit_text("Корзина пуста", reply_markup=builder.as_markup())

    msg = []
    for idx, i in enumerate(shopping_list.items, 1):
        text = f"{idx}. {i.name}"
        text = f"{text} / {i.storage} Гб" if i.storage else text
        text = f"{text} / {i.color}" if i.color else text
        price = await price_converter(i.price)
        subtotal = await price_converter(i.subtotal)
        total = f"\n🧾 <b><i>{i.quantity} * {price} = {subtotal} руб.</i></b>"
        text += total
        msg.append(text)

    total = await price_converter(shopping_list.total)
    msg.append(f"<b>Итого:</b> <b><i>{total} руб.</i></b>")
    msg = "\n\n".join(msg)
    builder.button(
        text="📝 Редактировать", callback_data="edit_shopping_list"
    )
    builder.button(
        text="« Назад в главное меню", callback_data="back_to_main"
    )
    builder.adjust(1)
    await callback.message.edit_text(msg, reply_markup=builder.as_markup())


@router.callback_query(Text("edit_shopping_list"))
@inject
async def edit_shopping_list(
    callback: CallbackQuery,
    use_case: SqlaShoppingListRepository = Provide[SqlaRepositoriesContainer.shopping_list_repository]
    ):
    ...