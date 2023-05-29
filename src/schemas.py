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
