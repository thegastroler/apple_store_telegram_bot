from .users import SqlaUsersRepository
from .categories import SqlaCategoriesRepository
from .items import SqlaItemsRepository
from .shopping_list import SqlaShoppingListRepository
from dependency_injector.containers import DeclarativeContainer
from dependency_injector.providers import Factory
from infrastructure.sql.container import SqlAlchemyContainer


class SqlaRepositoriesContainer(DeclarativeContainer):
    users_repository = Factory(
        SqlaUsersRepository, session_factory=SqlAlchemyContainer.session_factory.provided
    )
    category_repository = Factory(
        SqlaCategoriesRepository, session_factory=SqlAlchemyContainer.session_factory.provided
    )
    items_repository = Factory(
        SqlaItemsRepository, session_factory=SqlAlchemyContainer.session_factory.provided
    )
    shopping_list_repository = Factory(
        SqlaShoppingListRepository, session_factory=SqlAlchemyContainer.session_factory.provided
    )
