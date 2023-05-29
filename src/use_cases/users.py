from abc import ABC, abstractmethod
from contextlib import AbstractAsyncContextManager
from typing import Callable

from infrastructure.sql import models
from sqlalchemy import select, and_
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import AsyncSession
from schemas import UserSchema



class SqlaUsersRepository():
    model = models.User

    def __init__(self, session_factory: Callable[..., AbstractAsyncContextManager[AsyncSession]]):
        self.session_factory = session_factory

    async def create(self, chat_id: int, username: str):
        async with self.session_factory() as session:
            query = select(self.model).filter(and_(
                self.model.user_id == chat_id, self.model.username == username)
            )
            result = await session.execute(query)
            result = result.scalar_one_or_none()
            if not result:
                obj = UserSchema(user_id=chat_id, username=username)
                query = insert(self.model).values(obj.__dict__)
                await session.execute(query)
                await session.commit()
