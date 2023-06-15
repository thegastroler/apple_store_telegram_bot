from aiogram import F
from aiogram.filters import Text
from aiogram.types import CallbackQuery
from aiogram.utils.keyboard import InlineKeyboardBuilder
from dependency_injector.wiring import Provide, inject
from schemas import ShoppingListSchema
from use_cases import SqlaShoppingListRepository
from use_cases.container import SqlaRepositoriesContainer
from utils import price_converter

from . import router
from .callback_factories import EditShoppingListCallbackFactory


async def empty_shopping_list(callback: CallbackQuery, builder: InlineKeyboardBuilder):
    builder.button(text="« На главную страницу", callback_data="home")
    builder.adjust(1)
    return await callback.message.edit_text(
        "Корзина пуста", reply_markup=builder.as_markup()
    )


async def rednder_item_page(
    callback_data: EditShoppingListCallbackFactory,
    use_case: SqlaShoppingListRepository = Provide[
        SqlaRepositoriesContainer.shopping_list_repository
    ],
):
    """
    Отрисовка страницы товара в разделе редактирования корзины
    """
    num = callback_data.num
    order = callback_data.order

    item = await use_case.get_item_from_shopping_list(callback_data.order, num)

    text = item.name
    text = f"{text} / {item.storage} Гб" if item.storage else text
    text = f"{text} / {item.color}" if item.color else text
    price = await price_converter(item.price)
    subtotal = await price_converter(item.subtotal)
    total = f"\n🧾 <b><i>{item.quantity} * {price} = {subtotal} руб.</i></b>"
    text += total

    builder = InlineKeyboardBuilder()
    builder.button(
        text="❌ Удалить",
        callback_data=EditShoppingListCallbackFactory(
            id=item.id, action="del", num=num, order=order
        ),
    )

    if item.quantity == 1:
        builder.button(
            text="➖",
            callback_data=EditShoppingListCallbackFactory(
                id=item.id, action="del", num=num, order=order
            ),
        )
    else:
        builder.button(
            text="➖",
            callback_data=EditShoppingListCallbackFactory(
                id=item.id, action="decr", num=num, order=order
            ),
        )

    if item.quantity < item.total:
        builder.button(
            text="➕",
            callback_data=EditShoppingListCallbackFactory(
                id=item.id, action="incr", num=num, order=order
            ),
        )

    if item.len_shopping_list > 1:
        if num == item.len_shopping_list:
            builder.button(
                text="Следующий товар »",
                callback_data=EditShoppingListCallbackFactory(num=1, order=order),
            )
        else:
            builder.button(
                text="Следующий товар »",
                callback_data=EditShoppingListCallbackFactory(num=num + 1, order=order),
            )
    builder.button(text="« Назад в корзину", callback_data="shopping_list")
    builder.button(text="« На главную страницу", callback_data="home")

    if item.quantity < item.total:
        builder.adjust(3, 1)
    else:
        builder.adjust(2, 1)
    return text, builder


async def make_shopping_list(shopping_list: ShoppingListSchema) -> str:
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
    return msg


@router.callback_query(Text("shopping_list"))
@inject
async def shopping_list(
    callback: CallbackQuery,
    use_case: SqlaShoppingListRepository = Provide[
        SqlaRepositoriesContainer.shopping_list_repository
    ],
):
    """
    Корзина
    """
    user_id = callback.from_user.id
    shopping_list = await use_case.get_shopping_list(user_id)

    builder = InlineKeyboardBuilder()

    if not shopping_list.items:
        return await empty_shopping_list(callback, builder)

    msg = await make_shopping_list(shopping_list)

    builder.button(
        text="📝 Редактировать",
        callback_data=EditShoppingListCallbackFactory(
            action=None, num=1, order=shopping_list.order
        ),
    )
    builder.button(
        text="❌ Очистить корзину",
        callback_data=EditShoppingListCallbackFactory(
            action="confirm", order=shopping_list.order
        ),
    )
    builder.button(text="💳 К оплате", callback_data="pay")
    builder.button(text="« На главную страницу", callback_data="home")
    builder.adjust(1)
    await callback.message.edit_text(msg, reply_markup=builder.as_markup())


@router.callback_query(EditShoppingListCallbackFactory.filter(F.action == "confirm"))
@inject
async def confirm_clear_shopping_list(
    callback: CallbackQuery,
    callback_data: EditShoppingListCallbackFactory,
):
    """
    Подтверждение очистки корзины
    """
    builder = InlineKeyboardBuilder()
    builder.button(
        text="❌ Очистить корзину",
        callback_data=EditShoppingListCallbackFactory(
            action="clear", order=callback_data.order
        ),
    )
    builder.button(
        text="« Назад",
        callback_data="shopping_list",
    )
    builder.adjust(1)
    await callback.message.edit_text(
        "Вы точно хотите удалить все добавленные товары? Отменить данное действие будет невозможно.",
        reply_markup=builder.as_markup(),
    )


@router.callback_query(EditShoppingListCallbackFactory.filter(F.action == None))
@inject
async def edit_shopping_list(
    callback: CallbackQuery,
    callback_data: EditShoppingListCallbackFactory,
):
    """
    Редактирование корзины
    """
    text, builder = await rednder_item_page(callback_data)
    await callback.message.edit_text(text, reply_markup=builder.as_markup())


@router.callback_query(EditShoppingListCallbackFactory.filter(F.action != None))
@inject
async def edit_item_shopping_list(
    callback: CallbackQuery,
    callback_data: EditShoppingListCallbackFactory,
    use_case: SqlaShoppingListRepository = Provide[
        SqlaRepositoriesContainer.shopping_list_repository
    ],
):
    if callback_data.action == "incr":
        await use_case.increase_quantity_by_item_id(callback_data.id)
    elif callback_data.action == "decr":
        await use_case.decrease_quantity_by_item_id(callback_data.id)
    elif callback_data.action == "del":
        await use_case.del_item(callback_data.id)
    elif callback_data.action == "clear":
        await use_case.clear_shopping_list(callback_data.order)

        shopping_list = await use_case.get_shopping_list(callback.from_user.id)
        builder = InlineKeyboardBuilder()

        if not shopping_list.items:
            return await empty_shopping_list(callback, builder)

    text, builder = await rednder_item_page(callback_data)
    await callback.message.edit_text(text, reply_markup=builder.as_markup())
