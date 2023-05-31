from aiogram.types import CallbackQuery
from aiogram.utils.keyboard import InlineKeyboardBuilder
from dependency_injector.wiring import Provide, inject
from use_cases import SqlaCategoriesRepository, SqlaItemsRepository
from use_cases.container import SqlaRepositoriesContainer

from .. import router
from ..callback_factories import (CategoryCallbackFactory,
                                  ItemIdCallbackFactory,
                                  ItemIndexCallbackFactory,
                                  ItemIndexStorageCallbackFactory)


@router.callback_query(CategoryCallbackFactory.filter())
@inject
async def item_names(
    callback: CallbackQuery,
    callback_data: CategoryCallbackFactory,
    item_use_case: SqlaItemsRepository = Provide[SqlaRepositoriesContainer.items_repository],
    category_use_case: SqlaCategoriesRepository = Provide[SqlaRepositoriesContainer.category_repository]
    ):
    """
    Список названий товаров по категории
    """
    category_id = callback_data.id
    items_names = await item_use_case.get_items_by_category(category_id)
    category_name = await category_use_case.get_category_name(category_id)
    category_name = category_name[0]
    builder = InlineKeyboardBuilder()
    for i in items_names:
        builder.button(
            text=i[0],
            callback_data=ItemIndexCallbackFactory(
                item_index=i[1], category_id=category_id)
        )
    builder.button(
        text="◀️ Назад в категории", callback_data="items"
    )
    builder.adjust(1)
    await callback.message.edit_text(
        category_name,
        reply_markup=builder.as_markup(),
    )


@router.callback_query(ItemIndexCallbackFactory.filter())
@inject
async def item_storages(
    callback: CallbackQuery,
    callback_data: ItemIndexCallbackFactory,
    item_use_case: SqlaItemsRepository = Provide[SqlaRepositoriesContainer.items_repository],
    ):
    """
    Список объемов памяти и цен для выбранного товара
    """
    item_index = callback_data.item_index
    item_name = await item_use_case.get_item_name_by_index(item_index)
    item_name = item_name[0][0]
    storages = await item_use_case.get_item_storages(item_index)
    builder = InlineKeyboardBuilder()
    for i in storages:
        price = f"{str(i[2])[:-5]} {str(i[2])[2:-2]}"
        builder.button(
            text=f"{i[0]} Гб, {price} руб.",
            callback_data=ItemIndexStorageCallbackFactory(
                item_index=item_index, storage=i[0]
            )
        )
    builder.button(
        text="◀️ Назад к товару", callback_data=CategoryCallbackFactory(
            id=callback_data.category_id
        )
    )
    builder.button(
        text="◀️ Назад в категории", callback_data="items"
    )
    builder.adjust(1)
    await callback.message.edit_text(
        f"{item_name}, объем памяти:",
        reply_markup=builder.as_markup(),
    )


@router.callback_query(ItemIndexStorageCallbackFactory.filter())
@inject
async def item_colors(
    callback: CallbackQuery,
    callback_data: ItemIndexStorageCallbackFactory,
    item_use_case: SqlaItemsRepository = Provide[SqlaRepositoriesContainer.items_repository],
    ):
    """
    Список расцветок для выбранного товара
    """
    item_index = callback_data.item_index
    storage = callback_data.storage
    category_id = await item_use_case.get_category_by_item_index(item_index)
    category_id = category_id[0]
    colors = await item_use_case.get_item_colors(item_index, storage)
    item_name = colors[0][2]
    builder = InlineKeyboardBuilder()
    for i in colors:
        builder.button(
            text=f"{i[1]}",
            callback_data=ItemIdCallbackFactory(id=i[0])
        )
    builder.button(
        text="◀️ Назад к выбору памяти", callback_data=ItemIndexCallbackFactory(
            item_index=item_index, category_id=category_id
        )
    )
    builder.button(
        text="◀️ Назад в категории", callback_data="items"
    )
    builder.adjust(1)
    await callback.message.edit_text(
        f"{item_name} / <b>{storage} Гб</b>, цвет:",
        reply_markup=builder.as_markup(),
    )
