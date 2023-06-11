from contextlib import AbstractAsyncContextManager
from typing import Callable, List, Optional

from infrastructure.sql import models
from schemas import UserSchema
from sqlalchemy import and_, select, update
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import AsyncSession


class SqlaUsersRepository:
    model = models.User

    def __init__(
        self, session_factory: Callable[..., AbstractAsyncContextManager[AsyncSession]]
    ):
        self.session_factory = session_factory

    async def create(self, chat_id: int, username: str) -> UserSchema:
        async with self.session_factory() as session:
            query = select(self.model).filter(
                and_(self.model.user_id == chat_id, self.model.username == username)
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

    async def get_admins(self) -> Optional[List]:
        async with self.session_factory() as session:
            query = select(self.model.user_id).filter(self.model.is_admin == True)
            result = await session.execute(query)
            return [i[0] for i in result.fetchall()]

    async def get_banned(self) -> Optional[List]:
        async with self.session_factory() as session:
            query = select(self.model.user_id).filter(self.model.banned == True)
            result = await session.execute(query)
            return [i[0] for i in result.fetchall()]

    async def ban_user(self, username: str) -> Optional[str]:
        async with self.session_factory() as session:
            query = (
                update(self.model)
                .filter(self.model.username == username)
                .values({"banned": True})
                .returning(self.model.username)
            )
            result = await session.execute(query)
            result = result.scalar()
            await session.commit()
            return result

    async def unban_user(self, username: str) -> Optional[str]:
        async with self.session_factory() as session:
            query = (
                update(self.model)
                .filter(self.model.username == username)
                .values({"banned": False})
                .returning(self.model.username)
            )
            result = await session.execute(query)
            result = result.scalar()
            await session.commit()
            return result

    async def data_updating(self, user_id: int, username: str) -> None:
        async with self.session_factory() as session:
            query = select(self.model.username).filter(self.model.user_id == user_id)
            result = await session.execute(query)
            result = result.scalar()
            if result != username:
                query = (
                    update(self.model)
                    .filter(self.model.user_id == user_id)
                    .values({"username": username})
                )
                await session.execute(query)
                await session.commit()
