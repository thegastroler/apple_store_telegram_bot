from aiogram.types import CallbackQuery
from aiogram.filters import Command, Text
from aiogram.types import Message
from aiogram.utils.keyboard import InlineKeyboardBuilder
from dependency_injector.wiring import Provide, inject
from use_cases import SqlaCategoriesRepository, SqlaItemsRepository, SqlaShoppingCartRepository
from use_cases.container import SqlaRepositoriesContainer
from utils import price_converter

from . import router
from .callback_factories import (CategoryCallbackFactory,
                                  ItemIdCallbackFactory,
                                  ItemIndexCategoryCallbackFactory,
                                  ItemIndexStorageCallbackFactory)
from utils import make_order


@router.callback_query(Text("shopping_cart"))
@inject
async def item_names(
    callback: CallbackQuery,
    use_case: SqlaShoppingCartRepository = Provide[SqlaRepositoriesContainer.shopping_cart_repository]
    ):
    """
    Корзина
    """
    user_id = callback.from_user.id
    shopping_cart = await use_case.get_shopping_cart(user_id)
    msg = []
    for i in shopping_cart.items:
        text = i.name
        text = f"{text} / {i.storage} Гб" if i.storage else text
        text = f"{text} / {i.color}" if i.color else text
        text = f"{text}  |  {i.quantity} *"
        text = f"{text} {i.price}"
        text = f"{text} = {i.subtotal} руб."
        msg.append(text)
    msg.append(f"Итого: {shopping_cart.total} руб.")
    msg = "\n\n".join(msg)
    builder = InlineKeyboardBuilder()
    builder.button(
        text="« Назад в главное меню", callback_data="back_to_main"
    )
    builder.adjust(1)
    await callback.message.edit_text(msg, reply_markup=builder.as_markup())
