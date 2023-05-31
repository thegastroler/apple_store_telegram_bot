from contextlib import AbstractAsyncContextManager
from typing import Callable, List, Tuple

from infrastructure.sql import models
from schemas import CategorySchema
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession


class SqlaCategoriesRepository():
    m = models.Category

    def __init__(self, session_factory: Callable[..., AbstractAsyncContextManager[AsyncSession]]):
        self.session_factory = session_factory

    async def get_all(self) -> List[CategorySchema]:
        async with self.session_factory() as session:
            query = select(self.m)
            result = await session.execute(query)
            result = result.scalars()
        return [CategorySchema.from_orm(i) for i in result]

    async def get_category_name(self, category_id: int) -> Tuple[str]:
        async with self.session_factory() as session:
            query = select(self.m.name).filter(self.m.id == category_id)
            result = await session.execute(query)
            return result.one()
