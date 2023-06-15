from contextlib import asynccontextmanager
import logging
from typing import AsyncIterator

from aioredis import Redis, from_url
from worker.celeryconfig import broker_url

logger = logging.getLogger(__name__)


@asynccontextmanager
async def async_redis() -> AsyncIterator[Redis]:
    session = await from_url(broker_url)
    yield session
    await session.close()
