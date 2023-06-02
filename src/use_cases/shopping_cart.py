from contextlib import AbstractAsyncContextManager
from typing import Callable, List, Optional, Tuple

from infrastructure.sql import models
from sqlalchemy import and_, select, insert, update, desc
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession
from utils import make_order
from schemas import OrderIdSchema, IdQuantitySchema, TotalSchema

class SqlaShoppingCartRepository():
    m = models.ShoppingCart

    def __init__(self, session_factory: Callable[..., AbstractAsyncContextManager[AsyncSession]]):
        self.session_factory = session_factory

    async def add(self, user_id: int, item_id: int) -> None:
        unpaid_order = await self.get_unpaid_order(user_id)
        if unpaid_order:
            order = unpaid_order.order
            id_quantity = await self.get_id_quantity(order, item_id)
            if id_quantity:
                item_total = await self.get_item_quantity(order, item_id)
                if item_total.total > id_quantity.quantity:
                    return await self.increase_quantity(order, item_id)
            else:
                return await self.insert_row(user_id, item_id, order)
        else:
            last_order = await self.get_last_paid_order(user_id)
            if last_order:
                order = await make_order(order=last_order.order)
            else:
                order = await make_order(user_id=user_id)
            await self.insert_row(user_id, item_id, order)

    async def insert_row(self, user_id: int, item_id: int, order: str):
        async with self.session_factory() as session:
            query = insert(self.m)\
                .values({
                    "user_id": user_id,
                    "item_id": item_id,
                    "order": order,
                    "quantity": 1
                })
            await session.execute(query)
            await session.commit()

    async def get_unpaid_order(self, user_id: int) -> Optional[OrderIdSchema]:
        async with self.session_factory() as session:
            query = select(self.m.order)\
                .filter(and_(self.m.paid == False, self.m.user_id == user_id))
            result = await session.execute(query)
            result = result.first()
            order = result[0] if result else None
            return OrderIdSchema(order=order) if order else None

    async def get_last_paid_order(self, user_id: int) -> Optional[OrderIdSchema]:
        async with self.session_factory() as session:
            query = select(self.m.order)\
                .filter(and_(self.m.paid == True, self.m.user_id == user_id))\
                .order_by(desc(self.m.order))
            result = await session.execute(query)
            result = result.first()
            order = result[0] if result else None
            return OrderIdSchema(order=order) if order else None

    async def increase_quantity(self, order: str, item_id: int) -> List[Tuple[str]]:
        async with self.session_factory() as session:
            query = update(self.m).\
                where(and_(
                    self.m.order == order,
                    self.m.item_id == item_id)).\
                values({"quantity": self.m.quantity + 1})
            await session.execute(query)
            await session.commit()

    async def get_id_quantity(self, order: str, item_id: int) -> Optional[IdQuantitySchema]:
        async with self.session_factory() as session:
            query = select(self.m.id, self.m.quantity).\
                where(and_(
                    self.m.order == order,
                    self.m.item_id == item_id))
            result = await session.execute(query)
            result = result.first()
            return IdQuantitySchema(id=result[0], quantity=result[1]) if result else None

    async def get_item_quantity(self, order: str, item_id: int) -> List[Tuple[str]]:
        async with self.session_factory() as session:
            query = select(self.m).\
                where(and_(
                    self.m.order == order,
                    self.m.item_id == item_id)).\
                options(selectinload(self.m.item))
            result = await session.execute(query)
            result = result.scalars()
            return [TotalSchema(total=i.item.total) for i in result][0]
