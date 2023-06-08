from typing import Any, Awaitable, Callable, Dict

from aiogram import BaseMiddleware
from aiogram.types import CallbackQuery

from infrastructure.redis.db import async_redis


class IsBannedCallbackMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[CallbackQuery, Dict[str, Any]], Awaitable[Any]],
        event: CallbackQuery,
        data: Dict[str, Any],
    ) -> Any:
        user = data.get("event_from_user").id
        async with async_redis() as r:
            is_banned = await r.sismember("ban_list", user)
        if not is_banned:
            return await handler(event, data)
