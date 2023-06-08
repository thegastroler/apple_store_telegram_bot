from contextlib import AbstractAsyncContextManager
from typing import Callable, List, Optional, Tuple

from infrastructure.sql import models
from schemas import (
    EditItemShoppingListSchema,
    IdQuantitySchema,
    ItemShoppingListSchema,
    ItemTotalSchema,
    OrderIdSchema,
    ShoppingListSchema,
)
from sqlalchemy import and_, desc, insert, label, select, update, delete
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from utils import make_order


class SqlaShoppingListRepository:
    m = models.ShoppingList

    def __init__(
        self, session_factory: Callable[..., AbstractAsyncContextManager[AsyncSession]]
    ):
        self.session_factory = session_factory

    async def insert_row(self, user_id: int, item_id: int, order_id: str):
        async with self.session_factory() as session:
            query = insert(self.m).values(
                {
                    "user_id": user_id,
                    "item_id": item_id,
                    "order_id": order_id,
                    "quantity": 1,
                }
            )
            await session.execute(query)
            await session.commit()

    async def increase_quantity(self, order: str, item_id: int) -> List[Tuple[str]]:
        async with self.session_factory() as session:
            query = (
                update(self.m)
                .where(and_(self.m.order_id == order, self.m.item_id == item_id))
                .values({"quantity": self.m.quantity + 1})
            )
            await session.execute(query)
            await session.commit()

    async def increase_quantity_by_item_id(self, sl_id: int) -> List[Tuple[str]]:
        async with self.session_factory() as session:
            query = (
                update(self.m)
                .where(self.m.id == sl_id)
                .values({"quantity": self.m.quantity + 1})
            )
            await session.execute(query)
            await session.commit()

    async def decrease_quantity_by_item_id(
        self, id: int
    ) -> Optional[EditItemShoppingListSchema]:
        i = models.Item
        sl = self.m
        async with self.session_factory() as session:
            m = self.m
            query = (
                update(self.m)
                .where(self.m.id == id)
                .values({"quantity": self.m.quantity - 1})
            )
            await session.execute(query)
            await session.commit()
            query = (
                select(
                    sl.id,
                    i.name,
                    i.storage,
                    i.color,
                    sl.quantity,
                    i.price,
                    i.total,
                    label("subtotal", sl.quantity * i.price),
                )
                .select_from(sl)
                .join(i, i.id == sl.item_id)
                .where(m.id == id)
            )
            result = await session.execute(query)
            result = result.fetchall()
            return (
                [
                    EditItemShoppingListSchema(
                        id=i.id,
                        name=i.name,
                        storage=i.storage,
                        color=i.color,
                        quantity=i.quantity,
                        price=i.price,
                        subtotal=i.subtotal,
                        total=i.total,
                        len_shopping_list=len(result),
                    )
                    for i in result
                ][0]
                if result
                else None
            )

    async def get_id_quantity(
        self, order_id: str, item_id: int
    ) -> Optional[IdQuantitySchema]:
        async with self.session_factory() as session:
            query = select(self.m.id, self.m.quantity).where(
                and_(self.m.order_id == order_id, self.m.item_id == item_id)
            )
            result = await session.execute(query)
            result = result.first()
            return (
                IdQuantitySchema(id=result[0], quantity=result[1]) if result else None
            )

    async def get_item_quantity(self, order: str, item_id: int) -> List[Tuple[str]]:
        async with self.session_factory() as session:
            query = (
                select(self.m)
                .where(and_(self.m.order_id == order, self.m.item_id == item_id))
                .options(selectinload(self.m.item))
            )
            result = await session.execute(query)
            result = result.scalars()
            return [ItemTotalSchema(total=i.item.total) for i in result][0]

    async def get_shopping_list(self, user_id: int) -> Optional[ShoppingListSchema]:
        itm = models.Item
        sl = models.ShoppingList
        ordr = models.Order
        async with self.session_factory() as session:
            query = (
                select(
                    itm.name,
                    itm.storage,
                    itm.color,
                    sl.quantity,
                    itm.price,
                    label("subtotal", sl.quantity * itm.price),
                    sl.order_id,
                )
                .select_from(sl)
                .join(itm, itm.id == sl.item_id)
                .join(ordr, ordr.order == sl.order_id)
                .where(and_(ordr.user_id == user_id, ordr.paid == False))
                .order_by(sl.created_at)
            )
            result = await session.execute(query)
            result = result.fetchall()
            total = sum([i.subtotal for i in result])
            order = [i.order_id for i in result]
            order = order[0] if order else None
            return ShoppingListSchema(
                items=[
                    ItemShoppingListSchema(
                        name=i.name,
                        storage=i.storage,
                        color=i.color,
                        quantity=i.quantity,
                        price=i.price,
                        subtotal=i.subtotal,
                    )
                    for i in result
                ],
                total=total,
                order=order,
            )

    async def get_item_from_shopping_list(
        self, order: str, num: int
    ) -> EditItemShoppingListSchema:
        i = models.Item
        sl = self.m
        async with self.session_factory() as session:
            query = (
                select(
                    sl.id,
                    i.name,
                    i.storage,
                    i.color,
                    sl.quantity,
                    i.price,
                    i.total,
                    label("subtotal", sl.quantity * i.price),
                )
                .select_from(sl)
                .join(i, i.id == sl.item_id)
                .where(sl.order_id == order)
                .order_by(sl.created_at)
            )
            result = await session.execute(query)
            result = result.fetchall()
            result = [
                EditItemShoppingListSchema(
                    id=i.id,
                    name=i.name,
                    storage=i.storage,
                    color=i.color,
                    quantity=i.quantity,
                    price=i.price,
                    subtotal=i.subtotal,
                    total=i.total,
                    len_shopping_list=len(result),
                )
                for i in result
            ]
            if len(result) >= num:
                return result[num - 1]
            else:
                return result[0]

    async def del_item(self, sl_id: int) -> None:
        async with self.session_factory() as session:
            query = delete(self.m).filter(self.m.id == sl_id)
            await session.execute(query)
            await session.commit()

    async def clear_shopping_list(self, order: str) -> None:
        async with self.session_factory() as session:
            query = delete(self.m).filter(self.m.order_id == order)
            await session.execute(query)
            await session.commit()
