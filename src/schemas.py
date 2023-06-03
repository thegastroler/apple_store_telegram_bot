from typing import List, Optional

from pydantic import BaseModel


class UserSchema(BaseModel):
    user_id: int
    username: str
    is_admin: bool = False

    class Config:
        orm_mode = True


class CategorySchema(BaseModel):
    id: int
    name: str

    class Config:
        orm_mode = True


class ItemSchema(BaseModel):
    id: int
    name: str
    storage: int
    color: str
    article: str
    category_id: int
    price: int
    total: int

    class Config:
        orm_mode = True


class OrderIdSchema(BaseModel):
    order: str


class IdQuantitySchema(BaseModel):
    id: int
    quantity: int


class ItemTotalSchema(BaseModel):
    total: int


class ItemStorageSchema(BaseModel):
    id: Optional[int]
    storage: Optional[int]
    name: str
    price: int


class ItemShoppingListSchema(BaseModel):
    id: int
    name: str
    storage: Optional[int]
    color: Optional[str]
    quantity: int
    price: int
    subtotal: int

    class Config:
        orm_mode = True


class ShoppingListSchema(BaseModel):
    items: Optional[List[ItemShoppingListSchema]]
    total: Optional[int]
