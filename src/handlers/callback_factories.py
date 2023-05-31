from typing import Optional
from aiogram.filters.callback_data import CallbackData


class CategoryCallbackFactory(CallbackData, prefix="category"):
    id: int


class ItemIndexCallbackFactory(CallbackData, prefix="item_index"):
    item_index: int
    category_id: int


class ItemIndexStorageCallbackFactory(CallbackData, prefix="item_index_storage"):
    item_index: int
    storage: Optional[int]


class ItemIdCallbackFactory(CallbackData, prefix="item_id"):
    id: int
