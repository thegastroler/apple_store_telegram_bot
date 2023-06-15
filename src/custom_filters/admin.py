from aiogram.filters import BaseFilter
from aiogram.types import Message
from infrastructure.redis.db import async_redis


class AdminFilter(BaseFilter):
    async def __call__(self, message: Message) -> bool:
        user_id = message.from_user.id
        async with async_redis() as r:
            is_admin = await r.sismember("admin_list", user_id)
        if is_admin:
            return True
        return False