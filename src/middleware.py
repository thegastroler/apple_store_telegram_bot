from typing import Any, Awaitable, Callable, Dict

from aiogram import BaseMiddleware
from aiogram.types import CallbackQuery

from infrastructure.redis.db import async_redis
from use_cases.container import SqlaRepositoriesContainer
from use_cases.users import SqlaUsersRepository
from dependency_injector.wiring import Provide, inject


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


class UserDataCallbackMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[CallbackQuery, Dict[str, Any]], Awaitable[Any]],
        event: CallbackQuery,
        data: Dict[str, Any],
    ) -> Any:
        user_id = data.get("event_from_user").id
        username = data.get("event_from_user").username
        await self.check_data(user_id, username)
        async with async_redis() as r:
            is_banned = await r.sismember("ban_list", user_id)
        if not is_banned:
            return await handler(event, data)

    async def check_data(
        self,
        user_id: int,
        username: str,
        use_case: SqlaUsersRepository = Provide[
            SqlaRepositoriesContainer.users_repository
        ],
    ):
        await use_case.data_updating(user_id, username)
