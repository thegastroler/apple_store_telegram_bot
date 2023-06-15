import asyncio
import sys

from celery import Celery
from dependency_injector.wiring import Provide, inject
from infrastructure.redis.db import async_redis
from use_cases import SqlaRepositoriesContainer, SqlaUsersRepository, container

celery_app = Celery("worker")
celery_app.config_from_object("worker.celeryconfig")

celery_app.conf.beat_schedule = {
    "scheduled_task": {"task": "worker.app.celery_scheduled_task", "schedule": 300},
}


@celery_app.task
def celery_scheduled_task() -> None:
    container.wire(modules=[sys.modules[__name__]])
    loop = asyncio.get_event_loop()
    loop.run_until_complete(load_to_redis())


@inject
async def load_to_redis(
    use_case: SqlaUsersRepository = Provide[SqlaRepositoriesContainer.users_repository],
):
    admins = await use_case.get_admins()
    banned = await use_case.get_banned()
    async with async_redis() as r:
        pipe = r.pipeline()
        pipe.delete("admin_list", "ban_list")
        pipe.sadd("admin_list", *admins) if admins else None
        pipe.sadd("ban_list", *banned) if banned else None
        await pipe.execute()
