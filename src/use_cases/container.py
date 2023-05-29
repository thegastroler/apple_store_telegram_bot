from .users import SqlaUsersRepository
from .categories import SqlaCategorysRepository
from dependency_injector.containers import DeclarativeContainer
from dependency_injector.providers import Factory
from infrastructure.sql.container import SqlAlchemyContainer


class SqlaRepositoriesContainer(DeclarativeContainer):
    users_repository = Factory(
        SqlaUsersRepository, session_factory=SqlAlchemyContainer.session_factory.provided
    )
    category_repository = Factory(
        SqlaCategorysRepository, session_factory=SqlAlchemyContainer.session_factory.provided
    )
