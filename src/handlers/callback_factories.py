from typing import Optional, Literal
from aiogram.filters.callback_data import CallbackData


class CategoryCallbackFactory(CallbackData, prefix="category_id"):
    id: int


class ItemIndexCategoryCallbackFactory(CallbackData, prefix="item_index_category"):
    item_index: int
    category: int


class ItemIndexStorageCallbackFactory(CallbackData, prefix="item_index_storage"):
    item_index: int
    storage: Optional[int]


class ItemIdCallbackFactory(CallbackData, prefix="item_id"):
    id: int
    item_index: int
    storage: Optional[int]
    no_color: Optional[bool]
    category: Optional[int]


class EditShoppingListCallbackFactory(CallbackData, prefix="edit_sl"):
    id: Optional[int]
    order: str
    action: Optional[Literal["decr", "incr", "del", "clear"]]
    num: Optional[int]
