from typing import Optional
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


class TotalSchema(BaseModel):
    total: int


class ItemStorages(BaseModel):
    id: Optional[int]
    storage: Optional[int]
    name: str
    price: int
