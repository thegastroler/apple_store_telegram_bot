from contextlib import AbstractAsyncContextManager
from typing import Callable

from infrastructure.sql import models
from schemas import UserSchema
from sqlalchemy import and_, select
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import AsyncSession


class SqlaUsersRepository():
    model = models.User

    def __init__(self, session_factory: Callable[..., AbstractAsyncContextManager[AsyncSession]]):
        self.session_factory = session_factory

    async def create(self, chat_id: int, username: str) -> UserSchema:
        async with self.session_factory() as session:
            query = select(self.model).filter(and_(
                self.model.user_id == chat_id, self.model.username == username)
            )
            result = await session.execute(query)
            result = result.scalar_one_or_none()
            result = UserSchema.from_orm(result) if result else None
            if result is None:
                obj = UserSchema(user_id=chat_id, username=username)
                query = insert(self.model).values(obj.__dict__).returning(self.model)
                result = await session.execute(query)
                result = result.one()
                result = [UserSchema.from_orm(i) for i in result][0]
                await session.commit()
        return result

