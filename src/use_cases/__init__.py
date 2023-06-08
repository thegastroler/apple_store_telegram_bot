from .container import SqlaRepositoriesContainer
from .users import SqlaUsersRepository
from .categories import SqlaCategoriesRepository
from .items import SqlaItemsRepository
from .shopping_list import SqlaShoppingListRepository
from .orders import SqlaOrdersRepository

container = SqlaRepositoriesContainer()
