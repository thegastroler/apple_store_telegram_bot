import asyncio

import sys
from typing import List, Tuple
from celery import Celery
from dependency_injector.wiring import Provide, inject
from infrastructure.redis.db import async_redis
from infrastructure.sql.config import AsyncDatabaseSettings
from infrastructure.sql.db import Database
from use_cases import SqlaRepositoriesContainer, SqlaUsersRepository

celery_app = Celery("worker")
celery_app.config_from_object("worker.celeryconfig")

celery_app.conf.beat_schedule = {
    "scheduled_task": {"task": "worker.app.celery_scheduled_task", "schedule": 15},
}


@celery_app.task
def celery_scheduled_task() -> None:
    asyncio.run(scheduled_task())


async def scheduled_task() -> None:
    admins, banned = await get_from_db()
    async with async_redis() as r:
        pipe = r.pipeline()
        pipe.delete("admin_list", "ban_list")
        pipe.sadd("admin_list", *admins) if admins else None
        pipe.sadd("ban_list", *banned) if banned else None
        await pipe.execute()


async def get_from_db() -> Tuple[List]:
    settings = AsyncDatabaseSettings()
    db = Database(url=settings.url, debug=settings.debug)
    repo = SqlaUsersRepository(db.session)
    admins = await repo.get_admins()
    banned = await repo.get_banned()
    return admins, banned
