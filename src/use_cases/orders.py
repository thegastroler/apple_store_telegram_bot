from contextlib import AbstractAsyncContextManager
from typing import Callable, Optional

from infrastructure.sql import models
from schemas import OrderIdSchema, UserSchema
from sqlalchemy import and_, select
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import and_, desc, insert, label, select, update, delete


class SqlaOrdersRepository:
    m = models.Order

    def __init__(self, session_factory):
        self.session_factory = session_factory

    async def get_unpaid_order(self, user_id: int) -> OrderIdSchema:
        async with self.session_factory() as session:
            query = select(self.m.order).filter(
                and_(self.m.paid == False, self.m.user_id == user_id)
            )
            result = await session.execute(query)
            result = result.first()
            order = result[0] if result else None
            return OrderIdSchema(order=order)

    async def get_last_paid_order(self, user_id: int) -> OrderIdSchema:
        async with self.session_factory() as session:
            query = (
                select(self.m.order)
                .filter(and_(self.m.paid == True, self.m.user_id == user_id))
                .order_by(desc(self.m.order))
            )
            result = await session.execute(query)
            result = result.first()
            order = result[0] if result else None
            return OrderIdSchema(order=order)

    async def insert_row(self, user_id: int, order: str) -> None:
        async with self.session_factory() as session:
            query = insert(self.m).values(
                {
                    "user_id": user_id,
                    "order": order,
                }
            )
            await session.execute(query)
            await session.commit()

    async def is_paid_order(self, order: str) -> bool:
        async with self.session_factory() as session:
            query = select(self.m.paid).filter(self.m.order == order)
            result = await session.execute(query)
            result = result.scalar()
            return result

    async def update_info_on_paid(self, order: str, data: dict) -> None:
        async with self.session_factory() as session:
            name = data.get("name") if data.get("name") else None
            phone_number = (
                data.get("phone_number") if data.get("phone_number") else None
            )
            email = data.get("email") if data.get("email") else None
            state = data.get("state") if data.get("state") else None
            city = data.get("city") if data.get("city") else None
            street_line1 = (
                data.get("street_line1") if data.get("street_line1") else None
            )
            street_line2 = (
                data.get("street_line2") if data.get("street_line2") else None
            )
            post_code = data.get("post_code") if data.get("post_code") else None
            query = (
                update(self.m)
                .filter(self.m.order == order)
                .values(
                    {
                        "paid": True,
                        "name": name,
                        "phone_number": phone_number,
                        "email": email,
                        "state": state,
                        "city": city,
                        "street_line1": street_line1,
                        "street_line2": street_line2,
                        "post_code": post_code,
                    }
                )
            )
            await session.execute(query)
            await session.commit()
