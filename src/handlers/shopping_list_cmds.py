from aiogram.filters import Text
from aiogram import F
from aiogram.types import CallbackQuery
from aiogram.utils.keyboard import InlineKeyboardBuilder, InlineKeyboardMarkup, InlineKeyboardButton
from dependency_injector.wiring import Provide, inject
from use_cases import SqlaShoppingListRepository
from use_cases.container import SqlaRepositoriesContainer
from utils import price_converter

from . import router
from .callback_factories import EditShoppingListCallbackFactory


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
        text="📝 Редактировать", callback_data=EditShoppingListCallbackFactory(num=1)
    )
    builder.button(
        text="« Назад в главное меню", callback_data="back_to_main"
    )
    builder.adjust(1)
    await callback.message.edit_text(msg, reply_markup=builder.as_markup())


@router.callback_query(EditShoppingListCallbackFactory.filter(F.num))
@inject
async def edit_shopping_list(
    callback: CallbackQuery,
    callback_data: EditShoppingListCallbackFactory,
    use_case: SqlaShoppingListRepository = Provide[SqlaRepositoriesContainer.shopping_list_repository]
    ):
    """
    Редактирование корзины
    """
    user_id = callback.from_user.id
    num = callback_data.num
    order = await use_case.get_unpaid_order(user_id)
    item = await use_case.get_item_from_shopping_list(order.order, num)

    text = item.name
    text = f"{text} / {item.storage} Гб" if item.storage else text
    text = f"{text} / {item.color}" if item.color else text
    price = await price_converter(item.price)
    subtotal = await price_converter(item.subtotal)
    total = f"\n🧾 <b><i>{item.quantity} * {price} = {subtotal} руб.</i></b>"
    text += total

    builder = InlineKeyboardBuilder()
    builder.button(text="❌ Удалить", callback_data=EditShoppingListCallbackFactory(id=item.id, all=True))
    builder.button(text="➖", callback_data=EditShoppingListCallbackFactory(id=item.id, decrease=True))
    if item.quantity < item.total:
        builder.button(text="➕", callback_data=EditShoppingListCallbackFactory(id=item.id, increase=True))
    if item.len_shopping_list > 1:
        builder.button(text="Следующий товар »", callback_data="shopping_list")
    builder.button(text="« Назад в корзину", callback_data="shopping_list")
    builder.button(text="« Назад в главное меню", callback_data="back_to_main")

    if item.quantity < item.total:
        builder.adjust(3, 1)
    else:
        builder.adjust(2, 1)
    await callback.message.edit_text(text, reply_markup=builder.as_markup())


@router.callback_query(EditShoppingListCallbackFactory.filter(F.id))
@inject
async def edit_shopping_list(
    callback: CallbackQuery,
    callback_data: EditShoppingListCallbackFactory,
    use_case: SqlaShoppingListRepository = Provide[SqlaRepositoriesContainer.shopping_list_repository]
    ):
    user_id = callback.from_user.id