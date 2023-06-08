from contextlib import asynccontextmanager
import logging
from typing import AsyncGenerator

from redis.asyncio import Redis
from worker.celeryconfig import broker_url

logger = logging.getLogger(__name__)


@asynccontextmanager
async def async_redis() -> AsyncGenerator[Redis, None]:
    redis: Redis = await Redis.from_url(broker_url)
    try:
        yield redis
    except Exception as exc:
        logger.exception("Redis session closed because of exception")
        raise exc
    finally:
        await redis.close()
