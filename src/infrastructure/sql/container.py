from dependency_injector.containers import DeclarativeContainer
from dependency_injector.providers import Factory, Singleton

from .config import AsyncDatabaseSettings
from .db import Database


class SqlAlchemyContainer(DeclarativeContainer):
    settings = AsyncDatabaseSettings()
    db = Singleton(Database, url=settings.url, debug=settings.debug)
    session_factory = Factory(db.provided.session)
