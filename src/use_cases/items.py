from contextlib import AbstractAsyncContextManager
from typing import Callable, List, Optional, Tuple

from infrastructure.sql import models
from schemas import ItemStorageSchema
from sqlalchemy import and_, select
from sqlalchemy.ext.asyncio import AsyncSession


class SqlaItemsRepository():
    m = models.Item

    def __init__(self, session_factory: Callable[..., AbstractAsyncContextManager[AsyncSession]]):
        self.session_factory = session_factory

    async def get_items_by_category(self, category: int) -> List[Tuple[str]]:
        async with self.session_factory() as session:
            query = select(self.m.name, self.m.item_index)\
                .filter(and_(self.m.category_id == category, self.m.total > 0)).distinct()\
                .order_by(self.m.name)
            result = await session.execute(query)
            return result.fetchall()

    async def get_item_storages(self, item_index: int) -> List[Optional[ItemStorageSchema]]:
        async with self.session_factory() as session:
            query = select(self.m.storage, self.m.name, self.m.price)\
                .filter(and_(self.m.item_index == item_index,  self.m.total > 0))\
                .distinct()\
                .order_by(self.m.storage)
            result = await session.execute(query)
            result = result.fetchall()
            if len(result) == 1 and not result[0][0]:
                query = select(self.m.id, self.m.storage, self.m.name, self.m.price)\
                    .filter(and_(self.m.item_index == item_index,  self.m.total > 0))\
                    .distinct()
                result = await session.execute(query)
                result = result.fetchall()
                return [
                    ItemStorageSchema(
                        id=i.id,
                        storage=i.storage,
                        name=i.name,
                        price=i.price
                    )
                    for i in result]
            return [
                ItemStorageSchema(
                    storage=i.storage,
                    name=i.name,
                    price=i.price
                )
                for i in result]

    async def get_item_name_by_index(self, item_index: int) -> List[Tuple[str]]:
        async with self.session_factory() as session:
            query = select(self.m.name)\
                .filter(self.m.item_index == item_index)\
                .distinct()
            result = await session.execute(query)
            return result.fetchall()

    async def get_item_colors(self, item_index: int, storage: int) -> List[Tuple[str]]:
        async with self.session_factory() as session:
            query = select(self.m.id, self.m.color, self.m.name)\
                .filter(and_(self.m.item_index == item_index, self.m.storage == storage))\
                .distinct()\
                .order_by(self.m.id)
            result = await session.execute(query)
            return result.fetchall()

    async def get_category_by_item_index(self, item_index: int) -> Tuple[int]:
        async with self.session_factory() as session:
            query = select(self.m.category_id)\
                .filter(self.m.item_index == item_index)
            result = await session.execute(query)
            return result.first()
