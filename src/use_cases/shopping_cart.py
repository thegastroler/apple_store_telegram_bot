from contextlib import AbstractAsyncContextManager
from typing import Callable, List, Tuple

from infrastructure.sql import models
from sqlalchemy import and_, select, insert, update, func
from sqlalchemy.ext.asyncio import AsyncSession
from utils import make_order_id


class SqlaShoppingCartRepository():
    m = models.ShoppingCart

    def __init__(self, session_factory: Callable[..., AbstractAsyncContextManager[AsyncSession]]):
        self.session_factory = session_factory

    async def add(self, user_id: int, item_id: int) -> None:
        unpaid_order_id = await self.get_last_unpaid_order(user_id)
        if not unpaid_order_id:
            last_order_id = await self.get_last_paid_order(user_id)
            if not last_order_id:
                order_id = await make_order_id(user_id=user_id)
            else:
                order_id = await make_order_id(order_id=last_order_id)
        if unpaid_order_id:
            order_id = unpaid_order_id[0]
            """
            добавить проверку на наличие записи с order_id и item_id
            """
            return await self.increase_quantity(order_id, item_id)
        else:
            async with self.session_factory() as session:
                query = insert(self.m)\
                    .values({
                        "user_id": user_id,
                        "item_id": item_id,
                        "order_id": order_id,
                        "quantity": 1
                    })
                await session.execute(query)
                await session.commit()

    async def get_last_unpaid_order(self, user_id: int) -> List[Tuple[str]]:
        async with self.session_factory() as session:
            query = select(self.m.order_id)\
                .filter(and_(self.m.paid == False, self.m.user_id == user_id))
            result = await session.execute(query)
            return result.one_or_none()

    async def get_last_paid_order(self, user_id: int) -> List[Tuple[str]]:
        async with self.session_factory() as session:
            query = select(self.m.order_id)\
                .filter(and_(self.m.paid == True, self.m.user_id == user_id))
            result = await session.execute(query)
            return result.one_or_none()

    async def increase_quantity(self, order_id: str, item_id: int) -> List[Tuple[str]]:
        async with self.session_factory() as session:
            query = update(self.m).\
                where(and_(
                    self.m.order_id == order_id,
                    self.m.item_id == item_id)).\
                values({"quantity": self.m.quantity + 1})
            await session.execute(query)
            await session.commit()





    async def get_item_storages(self, item_index: int) -> List[Tuple[str]]:
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
            return result

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
