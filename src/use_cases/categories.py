from contextlib import AbstractAsyncContextManager
from typing import Callable, List

from config import TelegramSettings
from infrastructure.sql import models
from schemas import CategorySchema
from sqlalchemy import and_, select, update
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import AsyncSession


class SqlaCategorysRepository():
    model = models.Category

    def __init__(self, session_factory: Callable[..., AbstractAsyncContextManager[AsyncSession]]):
        self.session_factory = session_factory

    async def get_all(self) -> List[CategorySchema]:
        async with self.session_factory() as session:
            query = select(self.model)
            result = await session.execute(query)
            result = result.scalars()
        return [CategorySchema.from_orm(i) for i in result]

